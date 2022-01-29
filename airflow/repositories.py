import aiohttp
from dataclasses import dataclass
from datetime import datetime
import logging
import json
from typing import Iterable

from sqlalchemy.orm.session import Session
from sqlalchemy import select

from redis_client import redis_client
from serializers import FlightSearchCreate
from models import FlightSearch, FlightProvider, FlightInfo


@dataclass
class Repository:
    session: Session

    async def create_provider(self, name: str, url: str) -> FlightProvider:
        obj = FlightProvider(name=name, url=url)
        self.session.add(obj)
        try:
            await self.session.commit()
        except Exception as e:
            logging.info(e)
            return await self.session.rollback()
        else:
            await self.session.refresh(obj)

        return obj

    async def create_client_request(self, flight_search_request: FlightSearch) -> FlightSearch:
        flight_search = FlightSearch(
            departure_at=flight_search_request.departure_at,
            departure_airport=flight_search_request.departure_airport
        )

        if flight_search_request.currency_code:
            flight_search.currency_code = flight_search_request.currency_code
            flight_search_request.departure_back_at = flight_search_request.departure_back_at
            flight_search_request.departure_back_airport = flight_search_request.departure_back_airport

        self.session.add(flight_search)
        try:
            await self.session.commit()
        except Exception as e:
            print(e)
            return await self.session.rollback()
        else:
            await self.session.refresh(flight_search)
        return flight_search

    async def make_request(self, url, request: FlightSearchCreate, flight_search: FlightSearch):
        data = {
            'departure_at': str(request.departure_at),
            'departure_airport': request.departure_airport
        }
        if request.back:
            data.update(
                back=request.back,
                departure_back_at=str(request.departure_back_at),
                departure_back_airport=request.departure_back_airport
            )
        if request.arrival_airport:
            data.update(
                arrival_airport=request.arrival_airport
            )
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data) as resp:
                if resp.status == 200:
                    await self.create_flight_info(resp, flight_search)

    async def create_flight_info(self, res: aiohttp.ClientResponse, flight_search: FlightSearch):
        response = await res.json()

        if response:
            flights_ = []
            for list_ in response['there']:
                departure_at = datetime.fromisoformat(list_['flights']['segment']['dep']['at'])
                departure_airport = list_['flights']['segment']['dep']['airport']
                arrival_at = datetime.fromisoformat(list_['flights']['segment']['arr']['at'])
                arrival_airport = list_['flights']['segment']['arr']['airport']
                price = float(list_['pricing']['total'])
                currency = list_['pricing']['currency']
                if currency != 'KZT':
                    flight_ex_rate = await self.get_rate(currency)
                    price = price * float(flight_ex_rate)
                obj = FlightInfo(
                    departure_at=departure_at, departure_airport=departure_airport,
                    arrival_at=arrival_at, arrival_airport=arrival_airport,
                    price=price, currency="KZT",
                    flight_search_id=flight_search.id
                )
                flights_.append(obj)
            self.session.add_all(flights_)
            if res.host == 'provider_b':
                flight_search.complete()
            self.session.add(flight_search)
            try:
                await self.session.commit()
            except Exception as e:
                logging.info(e)
                await self.session.rollback()

    async def get_result_by_uuid(self, uuid) -> FlightSearch:
        result = await self.session.execute(select(FlightSearch).filter_by(uuid=uuid))
        obj = result.scalar()
        return obj

    async def get_providers(self) -> Iterable[FlightProvider]:
        result = await self.session.execute(select(FlightProvider))
        providers = result.scalars().all()
        return providers

    async def remove_provider_by_id(self, provider_id: int) -> bool:
        result = await self.session.execute(select(FlightProvider).filter_by(id=provider_id))
        obj = result.scalar()
        await self.session.delete(obj)
        try:
            await self.session.commit()
        except Exception:
            await self.session.rollback()
        else:
            return True

    async def get_rate(self, flight_currency):
        exchange_rate = json.loads(redis_client.get('currencies'))
        return exchange_rate[flight_currency]
