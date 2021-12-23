from typing import Any, List, Optional

from sqlalchemy import select, delete, insert, and_, update

from apps.auth.model import User
from apps.bank.dao.currency import get_code_rate_on_date
from apps.bank.models.invoice import Invoice, Statuses
from apps.bank.schemas.currency import CurrencyRateOnDate
from apps.bank.schemas.invoice import InvoiceCreate, InvoiceUpdate
from core.exceptions import NotExistException, invoice_change_exception
from db.session import SessionManager

db = SessionManager()


async def get(id: Any, user: User) -> Optional[Invoice]:
    select_stmt = select(Invoice)
    if not user.banker:
        select_stmt = select_stmt.where(Invoice.user_id == user.id)
    select_stmt = select_stmt.where(Invoice.id == id)
    async with db.obtain_session() as sess:
        result = (await sess.execute(select_stmt)).scalar_one_or_none()
    return result


async def get_list(user: User = None, skip: int = 0, limit: int = 100) -> List[Invoice]:
    select_stmt = select(Invoice)
    if user:
        select_stmt = select_stmt.where(Invoice.user_id == user.id)
    select_stmt = select_stmt.offset(skip).limit(limit)
    async with db.obtain_session() as sess:
        results = (await sess.execute(select_stmt)).scalars().all()
    return results


async def create_invoice(obj_in: InvoiceCreate,
                         user: User) -> Optional[Invoice]:
    curr_rate = CurrencyRateOnDate(code=obj_in.curr_code,
                                   date_start=obj_in.inv_date)
    rate = await get_code_rate_on_date(curr_rate)
    if not rate:
        raise NotExistException('Not found rate for this currency')

    insert_stmt = insert(Invoice).values(
        user_id=user.id,
        currency_id=rate.id,
        inv_date=obj_in.inv_date,
        curr_count=obj_in.curr_count).returning(Invoice)
    async with db.obtain_session() as sess:
        result = (await sess.execute(insert_stmt)).mappings().first()
    return result


async def update_invoice(obj_db: Invoice, obj_in: InvoiceUpdate,
                         user: User) -> Invoice:
    if obj_db.status != Statuses.progress:
        raise invoice_change_exception
    if not user.banker and obj_db.user_id != user.id:
        raise invoice_change_exception

    update_stmt = update(Invoice).where(Invoice.id == obj_db.id).values(
        obj_in.dict(exclude_unset=True)).returning(Invoice)
    async with db.obtain_session() as sess:
        result = (await sess.execute(update_stmt)).mappings().first()
    return result


async def remove(id: int, user: User) -> Any:
    async with db.obtain_session() as sess:
        await sess.execute(delete(Invoice).where(and_(
            Invoice.id == id,
            Invoice.user_id == user.id,
            Invoice.status == Statuses.progress
        )))
