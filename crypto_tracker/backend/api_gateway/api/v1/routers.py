from fastapi import APIRouter
from .endpoints import auth, assets

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(assets.router, prefix="/assets", tags=["Assets"])
# api_router.include_router(alerts.router, prefix="/alerts", tags=["Alerts"])