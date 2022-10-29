from fastapi import FastAPI

from backend.api.v1.api import api_router as api_router_v1  # deprecated
from backend.api.v2.api import api_router as api_router_v2
from backend.core.config import settings

app = FastAPI()
app.include_router(api_router_v1, prefix=settings.API_V1_STR)  # deprecated
app.include_router(api_router_v2, prefix=settings.API_V2_STR)
