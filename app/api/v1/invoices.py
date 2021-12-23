from typing import Any, List

from fastapi import APIRouter, Depends

from apps.auth.model import User
from apps.bank.dao import invoice
from apps.bank.schemas.invoice import InvoiceUpdate, InvoiceView, InvoiceCreate, InvoiceViewFull
from core.exceptions import NotExistException
from core.security import current_user_is_banker, get_current_user

router = APIRouter(prefix='/invoices', tags=['Invoices'])


@router.get('/', response_model=List[InvoiceViewFull],
            dependencies=[Depends(current_user_is_banker)])
async def list_invoices(skip: int = 0, limit: int = 100) -> Any:
    results = await invoice.get_list(skip=skip, limit=limit)
    return results


@router.get('/my', response_model=List[InvoiceViewFull])
async def list_my_invoices(user: User = Depends(get_current_user),
                           skip: int = 0, limit: int = 100) -> Any:
    results = await invoice.get_list(user=user, skip=skip, limit=limit)
    return results


@router.get('/{obj_id}', response_model=InvoiceViewFull)
async def get_invoice(obj_id: int, user: User = Depends(get_current_user)) -> Any:
    result = await invoice.get(id=obj_id, user=user)
    if not result:
        raise NotExistException()
    return result


@router.post('/create', response_model=InvoiceView, status_code=201)
async def create_invoice(item: InvoiceCreate, user: User = Depends(get_current_user)) -> Any:
    result = await invoice.create_invoice(obj_in=item, user=user)
    return result


@router.put('/{obj_id}', response_model=InvoiceView)
async def update_invoice(obj_id: int, item: InvoiceUpdate,
                         user: User = Depends(get_current_user)) -> Any:
    obj_db = await invoice.get(id=obj_id, user=user)
    if not obj_db:
        raise NotExistException()
    result = await invoice.update_invoice(obj_db=obj_db, obj_in=item, user=user)
    return result


@router.delete('/{obj_id}')
async def delete_invoice(obj_id: int, user: User = Depends(get_current_user)) -> Any:
    result = await invoice.remove(id=obj_id, user=user)
    return result
