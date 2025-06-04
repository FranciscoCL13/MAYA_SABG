from core.config import settings
from core.api import api_router
from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse


import logging

LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s:%(lineno)d %(message)s"
logging.basicConfig(level=settings.LOG_LEVEL.upper(), format=LOG_FORMAT)
# logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
# logging.getLogger("sqlalchemy.engine").setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.CONTEXT_API}/openapi.json",
    docs_url=f"{settings.CONTEXT_API}/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router, prefix=settings.CONTEXT_API)


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content=exc.detail)


app.add_exception_handler(HTTPException, http_exception_handler)

@app.get("/")
async def read_root():
    return {"status": "ok", "message": "FastAPI is running"}
