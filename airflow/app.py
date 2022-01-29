import asyncio
import json

from fastapi import FastAPI, Depends, Response

from sqlalchemy.orm.session import Session
import uvicorn

from airflow.repositories import Repository
from airflow.utils import parse_exchange_xml
from database import SessionLocal
from models import FlightSearch
from serializers import FlightSearchCreate


app = FastAPI()


async def get_db():
    session: Session = SessionLocal()
    try:
        yield session
    finally:
        await session.close()


@app.post('/search')
async def search_data(
    flight_search_request: FlightSearchCreate,
    session: Session = Depends(get_db)
):
    if flight_search_request.back and \
        not flight_search_request.departure_back_at or \
            not flight_search_request.departure_back_airport:
        return Response('Выберите обратный билет', status_code=400)

    repo = Repository(session)
    providers = await repo.get_providers()
    if not providers:
        return Response(status_code=404)

    flight_search = await repo.create_client_request(flight_search_request)

    if not flight_search:
        return Response(status_code=404)

    tasks = []
    for provider in providers:
        tasks.append(
            asyncio.create_task(
                repo.make_request(
                    provider.url + '/search', flight_search_request, flight_search
                )))
    asyncio.gather(*tasks)
    return Response(
        json.dumps(
            {
                'search_id': flight_search.uuid,
                'status': flight_search.state,
                'flights': flight_search.flights
            }
        ), status_code=200)


@app.get('/result/{search_id}')
async def provider_result(search_id: str, session: Session = Depends(get_db)):
    repo = Repository(session)
    result: FlightSearch = await repo.get_result_by_uuid(search_id)
    if not result:
        return Response('К сожалению запроса не существует', status_code=404)
    elif result.state == 'PENDING':
        return Response('Еще не готово')

    return result


@app.post('/api/create-provider')
async def create_provider(name: str, url: str, session: Session = Depends(get_db)):
    repo = Repository(session)
    obj = await repo.create_provider(name, url)
    if not obj:
        return Response(status_code=404)
    return Response(
        'Поставщик создан с номером {}'.format(obj.id), status_code=200
    )


@app.get('/api/providers-list')
async def get_providers_list(session: Session = Depends(get_db)):
    repo = Repository(session)
    list_ = await repo.get_providers()
    return list_


@app.put('/api/remove-provider/{provider_id}')
async def remove_provider(provider_id: int, session: Session = Depends(get_db)):
    repo = Repository(session)
    if not await repo.remove_provider_by_id(provider_id):
        return Response(status_code=404)
    return Response('Провайдер удален', status_code=200)


def main():
    asyncio.run(parse_exchange_xml())
    uvicorn.run('app:app', host='0.0.0.0', port=9000, reload=True)


if __name__ == '__main__':
    main()
