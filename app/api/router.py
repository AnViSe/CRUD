from fastapi import APIRouter

from api.v1 import users, invoices, currencies
from core.config import settings

router_api_v1 = APIRouter(prefix=settings.API_V1_STR)

router_api_v1.include_router(users.router)
router_api_v1.include_router(invoices.router)
router_api_v1.include_router(currencies.router)
