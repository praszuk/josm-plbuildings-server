from fastapi import APIRouter

from backend.api.v2 import buildings, profiles

api_router = APIRouter()
api_router.include_router(buildings.router, prefix='/buildings', tags=['buildings'])
api_router.include_router(profiles.router, prefix='/profiles', tags=['profiles'])
