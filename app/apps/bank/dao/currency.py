from datetime import datetime, timedelta
from typing import Any, Optional, List

from sqlalchemy import and_, desc, func, select, delete, insert, update

from apps.bank.models.currency import Currency
from apps.bank.schemas.currency import CurrencyCreate, CurrencyRateOnDate, CurrencyUpdate
from apps.bank.utils.nbrb_rates import get_rate_date_code
from db.dao import DaoBase
from db.session import SessionManager

db = SessionManager()


class DaoCurrency(DaoBase[Currency]):
    pass


currency = DaoCurrency(Currency)


async def get(id: Any) -> Optional[Currency]:
    select_stmt = select(Currency).where(Currency.id == id)
    async with db.obtain_session() as sess:
        result = (await sess.execute(select_stmt)).scalar_one_or_none()
    return result


async def get_code_rate_on_date(item: CurrencyRateOnDate) -> Optional[Currency]:
    select_stmt = select(Currency).where(
        and_(func.upper(Currency.code) == func.upper(item.code),
             Currency.date_start <= item.date_start)
    ).order_by(desc(Currency.date_start)).limit(1)
    async with db.obtain_session() as sess:
        result = (await sess.execute(select_stmt)).scalar_one_or_none()
    return result


async def get_list(skip: int = 0, limit: int = 100) -> List[Currency]:
    select_stmt = select(Currency).offset(skip).limit(limit)
    async with db.obtain_session() as sess:
        results = (await sess.execute(select_stmt)).scalars().all()
    return results


async def create_currency(obj_in: CurrencyCreate) -> Optional[Currency]:
    insert_stmt = insert(Currency).values(obj_in.dict()).returning(Currency)
    async with db.obtain_session() as sess:
        result = (await sess.execute(insert_stmt)).mappings().first()
    return result


async def update_currency(obj_db: Currency, obj_in: CurrencyUpdate) -> Currency:
    update_stmt = update(Currency).where(Currency.id == obj_db.id).values(
        obj_in.dict(exclude_unset=True)).returning(Currency)
    async with db.obtain_session() as sess:
        result = (await sess.execute(update_stmt)).mappings().first()
    return result


async def remove_currency(id: int) -> Any:
    delete_stmt = delete(Currency).where(Currency.id == id)
    async with db.obtain_session() as sess:
        await sess.execute(delete_stmt)


async def import_rate_start_date(date_start: str = None):
    if not date_start:
        last_date_stmt = select(func.max(Currency.date_start))
        async with db.obtain_session() as sess:
            max_date = (await sess.execute(last_date_stmt)).scalar_one_or_none()
        if not max_date:
            start_date = datetime.now() + timedelta(days=-3)
        else:
            start_date = max_date + timedelta(days=1)
    else:
        start_date = datetime.strptime(date_start, '%Y-%m-%d')

    list_rates = await get_rate_date_code(start_date.strftime('%Y-%m-%d'))
    curr_items = []
    for rate in list_rates:
        curr_items.append(Currency(code=rate['Cur_Abbreviation'],
                                   scale=rate['Cur_Scale'],
                                   rate=rate['Cur_OfficialRate'],
                                   date_start=datetime.strptime(rate['Date'][0:10], '%Y-%m-%d')))

    async with db.obtain_session() as sess:
        sess.add_all(curr_items)
    return {'Loaded rates starts after date': start_date}
