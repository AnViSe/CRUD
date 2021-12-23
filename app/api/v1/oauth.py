from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from apps.auth import dao
from apps.auth.schema import UserRegister, UserView
from core.exceptions import login_invalid_exception, user_or_email_already_exist
from core.security import create_access_token
from core.utils import verify_password

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post('/register', response_model=UserView, summary='Регистрация')
async def auth_register(user: UserRegister):
    result = await dao.check_username_or_email(user.username, user.email)
    if result:
        raise user_or_email_already_exist
    return await dao.create_user(user)


@router.post('/login', summary='Авторизация')
async def auth_login(credentials: OAuth2PasswordRequestForm = Depends()):
    user = await dao.get_user_by_name(credentials.username)
    if not user:
        raise login_invalid_exception
    if not verify_password(credentials.password, user.password):
        raise login_invalid_exception
    access_token = create_access_token(data={'sub': credentials.username})
    return {
        'access_token': access_token,
        'token_type': 'bearer',
        'user_info': {
            'email': user.email,
        }
    }
