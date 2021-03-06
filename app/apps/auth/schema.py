import decimal
from typing import Optional, Any

# from email_validator import validate_email
from pydantic import BaseModel, Field, validator


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class UserBase(BaseModel):
    email: Optional[str] = Field(None, title='Адрес e-mail', example='user@example.com')

    # @validator('email')
    # def _validate_email(cls, v: Any) -> Optional[str]:
    #     if v:
    #         if not validate_email(v):
    #             raise ValueError('E-mail invalid')
    #     return v


class UserView(UserBase):
    id: int = Field(..., title='ID')
    username: str = Field(..., title='Имя пользователя')
    banker: bool = Field(..., title='Признак банкира')

    class Config:
        orm_mode = True


class UserViewMe(UserBase):
    id: int = Field(..., title='ID')
    username: str = Field(..., title='Имя пользователя')
    balance: decimal.Decimal = Field(..., title='Баланс')
    banker: bool = Field(..., title='Признак банкира')

    class Config:
        orm_mode = True


class UserViewJoin(BaseModel):
    username: str = Field(..., title='Имя пользователя')

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    username: str = Field(..., title='Имя пользователя', example='User')
    password: str = Field(..., title='Пароль', example='password')
    balance: Optional[decimal.Decimal] = Field(0, title='Баланс')
    banker: Optional[bool] = Field(False, title='Признак банкира')


class UserRegister(UserBase):
    username: str = Field(..., title='Имя пользователя', example='User')
    password: str = Field(..., title='Пароль', example='password')


class UserUpdate(UserBase):
    balance: Optional[decimal.Decimal] = Field(None, title='Баланс')
    banker: Optional[bool] = Field(None, title='Признак банкира')


class UserForgotPassword(UserBase):
    pass
