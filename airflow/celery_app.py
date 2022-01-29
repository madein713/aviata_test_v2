import asyncio

from celery import Celery
from celery.schedules import crontab

from utils import parse_exchange_xml

app = Celery()
app.conf.timezone = 'UTC'


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=00, minute=00),
        get_exchange_rate.s(),
        name='execute every midnight'
    )


@app.task
def get_exchange_rate():
    asyncio.run(parse_exchange_xml())
