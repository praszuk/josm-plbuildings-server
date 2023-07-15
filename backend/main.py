from urllib.parse import urlencode

from fastapi import FastAPI, Request

from backend.api.v1.api import api_router as api_router_v1  # deprecated
from backend.api.v2.api import api_router as api_router_v2
from backend.core.config import settings

app = FastAPI()
app.include_router(api_router_v1, prefix=settings.API_V1_STR)  # deprecated
app.include_router(api_router_v2, prefix=settings.API_V2_STR)


@app.middleware('http')
async def flatten_query_string_lists(request: Request, call_next):
    """
    Allow to pass list arguments like this:
    - &param=1,2,3
    instead of doing this:
    - &param=1&param=2&param=3
    https://github.com/tiangolo/fastapi/issues/50#issuecomment-1042362633
    """
    flattened = []
    for key, value in request.query_params.multi_items():
        flattened.extend((key, entry) for entry in value.split(','))

    request.scope['query_string'] = urlencode(flattened, doseq=True).encode(
        'utf-8'
    )

    return await call_next(request)
