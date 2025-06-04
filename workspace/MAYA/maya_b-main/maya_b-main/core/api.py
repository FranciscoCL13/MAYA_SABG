from fastapi import APIRouter
from endpoints import router
from endpoints import mapas

api_router = APIRouter()
api_router.include_router(router, prefix="", tags=["main"])
api_router.include_router(mapas.router, prefix="/mapas", tags=["mapas"])
