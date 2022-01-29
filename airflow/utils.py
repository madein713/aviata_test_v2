import aiohttp
import datetime
import xmltodict
import json
from redis_client import redis_client


async def parse_exchange_xml():
    items = {}
    async with aiohttp.ClientSession() as session:
        date_ = datetime.datetime.now().date().strftime('%d.%m.%Y')
        resp = await session.get(
            f'https://www.nationalbank.kz/rss/get_rates.cfm?fdate={date_}')
        data = await resp.read()
        parsed = xmltodict.parse(data)
        for key, value in parsed['rates'].items():
            if key == 'item':
                for currency in value:
                    items[currency['title']] = currency['description']

    redis_client.set('currencies', json.dumps(items))
