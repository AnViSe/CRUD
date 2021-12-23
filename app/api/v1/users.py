from typing import Any, List

from fastapi import APIRouter, Depends

from apps.auth import dao
from apps.auth.model import User
from apps.auth.schema import UserUpdate, UserView, UserCreate, UserViewMe
from core.exceptions import NotExistException
from core.security import get_current_user

router = APIRouter(prefix='/users', tags=['Users'])


@router.get('/', response_model=List[UserView])
async def list_users(skip: int = 0, limit: int = 100) -> Any:
    results = await dao.get_list(skip=skip, limit=limit)
    return results


@router.get('/me', response_model=UserViewMe)
async def get_user_me(current_user: User = Depends(get_current_user)) -> User:
    return current_user


@router.get('/{obj_id}', response_model=UserView)
async def get_user(obj_id: int) -> Any:
    obj_db = await dao.get(id=obj_id)
    if not obj_db:
        raise NotExistException()
    return obj_db


@router.post('/create', response_model=UserView, status_code=201)
async def create_user(item: UserCreate) -> Any:
    return await dao.create_user(obj_in=item)


@router.put('/{obj_id}', response_model=UserView)
async def update_user(obj_id: int,
                      item: UserUpdate,
                      user: User = Depends(get_current_user)) -> Any:
    obj_db = await dao.get(id=obj_id)
    if not obj_db:
        raise NotExistException()
    return await dao.update_user(obj_db=obj_db, obj_in=item, user=user)
