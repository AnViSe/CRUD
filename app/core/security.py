import time
from datetime import datetime, timedelta

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from apps.auth import dao
from apps.auth.model import User
from apps.auth.schema import TokenData
from core.config import settings
from core.exceptions import credentials_exception

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='auth/login')


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
        if payload.get('exp') < time.time():
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await dao.get_user_by_name(user_name=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def current_user_is_banker(current_user: User = Depends(get_current_user)):
    if not current_user.banker:
        raise credentials_exception


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def get_token_user(token: str = Depends(oauth2_scheme)):
    return token
