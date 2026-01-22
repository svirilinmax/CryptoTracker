from fastapi import APIRouter

from .endpoints import assets, auth

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(assets.router, prefix="/assets", tags=["Assets"])
