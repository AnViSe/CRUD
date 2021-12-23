import asyncio
import json
from datetime import datetime, timedelta
from string import Template
from typing import List

import httpx
from dateutil.rrule import DAILY, rrule

from core.config import settings


async def get_rate_date_code(date: str, code: str = None):
    """
    https://www.nbrb.by/api/exrates/rates/USD?parammode=2&ondate=2021-11-01
    https://www.nbrb.by/api/exrates/rates?ondate=2021-11-01&periodicity=0
    """
    q = asyncio.Queue(maxsize=50)
    response = []
    consumers = []
    producers = []

    dt_start = datetime.strptime(date, '%Y-%m-%d')
    dt_stop = datetime.now() + timedelta(days=3)
    for dt in rrule(DAILY, dtstart=dt_start, until=dt_stop):
        consumers.append(_consumer(q, response))
        producers.append(_producer(q, dt.strftime('%Y-%m-%d'), code))

    await asyncio.gather(*producers)
    await asyncio.gather(*consumers)
    return response


async def _get_rate(date: str, code: str = None):
    if not code:
        url = Template(settings.NBRB_RATES_DATE_URL).substitute(date=date)
    else:
        url = Template(settings.NBRB_RATES_CODE_URL).substitute(code=code, date=date)

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
    result = json.loads(response.text)
    return result


async def _producer(queue: asyncio.Queue, date: str, code: str = None):
    await queue.put(_get_rate(date=date, code=code))


async def _consumer(queue: asyncio.Queue, resp: List):
    result = await (await queue.get())
    if isinstance(result, list):
        resp.extend(result)
    else:
        resp.append(result)
