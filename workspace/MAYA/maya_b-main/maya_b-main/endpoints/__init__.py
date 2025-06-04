import logging

from fastapi import APIRouter
from core.config import settings
from typing import Any

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/version")
async def get_version() -> Any:
    return {"revision": settings.VERSION, "tag": settings.TAG}
