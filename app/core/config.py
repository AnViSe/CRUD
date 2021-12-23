# Конфигурация проекта
import logging.config
from functools import lru_cache
from logging import Logger
from pathlib import Path

from pydantic import BaseSettings
from starlette.config import Config

BASE_DIR = Path(__file__).resolve().parent.parent
config = Config(str(BASE_DIR) + '/.env')


class Settings(BaseSettings):
    DEBUG: bool = config('DEBUG', cast=bool, default=True)
    FUTURE: bool = config('FUTURE', cast=bool, default=True)  # Use 2.0 SQLAlchemy style
    API_V1_STR: str = '/api/v1'
    SECRET_KEY: str = config('SECRET_KEY', cast=str,
                             default='FaOsibHOugjgCdQDAaC6Apnblx9m6aF6FPgHqAA/3WnSKD')
    ALGORITHM: str = config('ALGORITHM', cast=str, default='HS256')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = config('ACCESS_TOKEN_EXPIRE_MINUTES', cast=int, default=30)

    PROJECT_NAME: str = config('PROJECT_NAME', cast=str,
                               default='CRUD Project')
    PROJECT_DESCRIPTION: str = config('PROJECT_DESCRIPTION', cast=str,
                                      default='CRUD Project descriptions')
    PROJECT_VERSION: str = config('PROJECT_VERSION', cast=str,
                                  default='0.0.1')

    TIMEZONE: str = config('TIMEZONE', cast=str, default='Europe/Minsk')

    SQLALCHEMY_DATABASE_URL_ASYNC: str = config('SQLALCHEMY_DATABASE_URL_ASYNC', cast=str,
                                                default='sqlite+aiosqlite:///./crud.db')
    SQLALCHEMY_DATABASE_URL_SYNC: str = config('SQLALCHEMY_DATABASE_URL_SYNC', cast=str,
                                               default='sqlite:///./crud.db')

    NBRB_RATES_CODE_URL: str = config(
        'NBRB_RATES_CODE_URL', cast=str,
        default='https://www.nbrb.by/api/exrates/rates/$code?parammode=2&ondate=$date')
    NBRB_RATES_DATE_URL: str = config(
        'NBRB_RATES_DATE_URL', cast=str,
        default='https://www.nbrb.by/api/exrates/rates?ondate=$date&periodicity=0')

    CELERY_BROKER_URL: str = config('CELERY_BROKER_URL', cast=str,
                                    default='redis://172.16.100.227:6379/10')
    CELERY_BACKEND_URL: str = config('CELERY_BACKEND_URL', cast=str,
                                     default='redis://172.16.100.227:6379/10')


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'default_formatter': {
            'format': '%(asctime)s [%(name)s] => %(levelname)s: %(message)s',
            'datefmt': '%Y.%m.%d %H:%M:%S',
        },
        'uvicorn_formatter': {
            '()': 'uvicorn.logging.DefaultFormatter',
            'format': '%(levelprefix)s %(asctime)s: %(message)s',
            'datefmt': '%Y.%m.%d %H:%M:%S',
        },
    },

    'handlers': {
        'file_handler': {
            'class': 'logging.FileHandler',
            'formatter': 'default_formatter',
            'filename': str(BASE_DIR) + '/logs/main.log',
            'encoding': 'UTF-8',
        },
        'file_handler_db': {
            'class': 'logging.FileHandler',
            'formatter': 'default_formatter',
            'filename': str(BASE_DIR) + '/logs/db.log',
            'encoding': 'UTF-8',
        },
        'stream_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'default_formatter',
            'stream': 'sys.stdout',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'uvicorn_formatter',
            'stream': 'ext://sys.stderr',
            'level': 'DEBUG',
        },
    },
    'loggers': {
        'main': {
            'handlers': ['file_handler'],
            'level': 'DEBUG',
            'propagate': True
        },
        'db.session': {
            'handlers': ['file_handler_db'],
            'level': 'DEBUG',
            'propagate': True
        },
    }
}


def init_logging(name: str = 'main') -> Logger:
    logging.config.dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger(name)

    return logger
