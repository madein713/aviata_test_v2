
import asyncio
from fastapi import FastAPI, Depends, Response

from provider_a.repository import FlightRepository

from serializers import FlightSearchCreate

app = FastAPI()


@app.post('/search')
async def flight_search(
    request: FlightSearchCreate,
    repo: FlightRepository = Depends(FlightRepository)
) -> Response:
    flights = await repo.get_flights(request)
    if not flights:
        return Response('По данному направлению нет рейсов', status_code=204)
    await asyncio.sleep(30)
    return flights
