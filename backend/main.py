from collections import OrderedDict
from logging import getLogger
from urllib.parse import urlencode

from fastapi import FastAPI, Request
from pythonjsonlogger import jsonlogger

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

    request.scope['query_string'] = urlencode(flattened, doseq=True).encode('utf-8')

    return await call_next(request)


@app.middleware('http')
async def log_access(request: Request, call_next):
    def merge_query_params(query_params) -> str:
        """
        data_sources=BDOT&data_sources=EGiB&lat=12&lon=12 -> data_sources=BDOT,EGiB&lat=12&lon=12
        """
        params = OrderedDict()
        for pair in query_params.split('&'):
            key, value = pair.split('=')
            if key not in params:
                params[key] = []
            params[key].append(value)

        return '&'.join(f'{k}={",".join(v)}' for k, v in params.items())

    client_addr = request.client.host if request.client else 'Unknown'
    if request.url.query:
        merged_query_params = merge_query_params(request.url.query)
        request_line = (
            f'{request.method} {request.url.path}'
            f'?{merged_query_params} HTTP/{request.scope["http_version"]}'
        )
    else:
        request_line = f'{request.method} {request.url.path} HTTP/{request.scope["http_version"]}'
    user_agent = request.headers.get('user-agent', 'Unknown')

    response = await call_next(request)
    status_code = response.status_code

    access_logger = getLogger(settings.ACCESS_LOGGER)
    access_logger.info(
        '',
        extra={
            'client_addr': client_addr,
            'request_line': request_line,
            'status_code': status_code,
            'user_agent': user_agent,
        },
    )
    return response


class AccessJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(AccessJsonFormatter, self).add_fields(log_record, record, message_dict)
        log_record['client_addr'] = log_record.get('client_addr', 'Unknown')
        log_record['request_line'] = log_record.get('request_line', 'Unknown')
        log_record['status_code'] = log_record.get('status_code', 'Unknown')
        log_record['user_agent'] = log_record.get('user_agent', 'Unknown')
