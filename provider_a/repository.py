from dataclasses import dataclass
from datetime import date, datetime
from serializers import FlightSearchCreate
from config.settings import settings
import aiofiles
import json
from pprint import pprint


@dataclass
class FlightRepository:
    json_path: str = settings.STATIC_DATA + '/response_a.json'

    async def get_flights(self, request: FlightSearchCreate):
        suitable_flight = {
            'there': []
        }
        async with aiofiles.open(self.json_path, mode='r') as f:
            data = json.loads(await f.read())
            for temp in data:
                for flight in temp['flights']:
                    for segment in flight['segments']:
                        dep_dt = datetime.fromisoformat(segment['dep']['at'])
                        dep_airport = segment['dep']['airport']
                        arr_airport = segment['arr']['airport']
                        data = {
                            'flights': {
                                'segment': segment
                            },
                            'pricing': {
                                'currency': temp['pricing']['currency'],
                                'total': temp['pricing']['total']
                            }
                        }
                        if request.departure_at == dep_dt.date() and \
                            request.departure_airport == dep_airport and \
                                request.arrival_airport == arr_airport:
                            suitable_flight['there'].append(data)
                        if request.back:
                            if request.departure_back_at == dep_dt.date() \
                                    and request.departure_back_airport == dep_airport:
                                try:
                                    suitable_flight['back'].append(data)
                                except KeyError:
                                    suitable_flight.update(back=[data])
        return suitable_flight
