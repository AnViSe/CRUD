from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from apps.auth.crud import get_user_auth
from core.exceptions import login_invalid_exception
from core.security import create_access_token
from core.utils import verify_password

auth_router = APIRouter(tags=['Auth'])


@auth_router.post('/login')
async def auth_login(credentials: OAuth2PasswordRequestForm = Depends()):
    user = await get_user_auth(credentials.username)
    if not user:
        raise login_invalid_exception
    if not verify_password(credentials.password, user.password):
        raise login_invalid_exception
    access_token = create_access_token(data={'sub': user.username})
    return {'access_token': access_token, 'token_type': 'bearer'}
