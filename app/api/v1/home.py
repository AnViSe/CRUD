from fastapi import APIRouter

from apps.bank.dao.currency import import_rate_start_date
from core.config import settings

router = APIRouter(tags=['Home'])


@router.get('/')
async def home():
    return {'Welcome to API': settings.PROJECT_NAME}


@router.get('/rate/{date}')
async def home(date: str = None):
    # result = await import_rate_start_date(date)
    result = await import_rate_start_date()
    return result
