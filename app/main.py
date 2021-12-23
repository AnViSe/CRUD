# Основной файл проекта
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

import core.events
from api.router import router_api_v1
from api.v1 import home, oauth, tasks

from core.config import init_logging, settings
from core.exceptions import ProjectException

logger = init_logging(__name__)

app = FastAPI(title=settings.PROJECT_NAME,
              description=settings.PROJECT_DESCRIPTION,
              version=settings.PROJECT_VERSION,
              openapi_url=f'{settings.API_V1_STR}/openapi.json',
              debug=settings.DEBUG)

# app.include_router(tasks.router)
# app.include_router(home.router)
app.include_router(oauth.router)
app.include_router(router_api_v1)


@app.exception_handler(ProjectException)
async def unicorn_exception_handler(request: Request, exc: ProjectException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            'code': exc.status_code,
            'message': exc.detail
        },
        headers=exc.headers,
    )


if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
