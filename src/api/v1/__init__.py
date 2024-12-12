from fastapi import APIRouter
from src.api.v1.views import router as router_v1

router = APIRouter()

router.include_router(router_v1)
