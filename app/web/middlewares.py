import json
import typing

from aiohttp.web_middlewares import middleware
from aiohttp_apispec.middlewares import validation_middleware
from aiohttp.web_exceptions import HTTPException, HTTPUnprocessableEntity

from app.web.utils import error_json_response

if typing.TYPE_CHECKING:
    from app.web.app import Application


@middleware
async def error_handling_middleware(request, handler):
    try:
        response = await handler(request)
        return response
    except HTTPException as e:
        return error_json_response(http_status=400, status='bad request', msg=e.reason, data=json.load(e.text))
    except HTTPUnprocessableEntity as e1:
        return error_json_response(http_status=e.status, status='error', msg=str(e1))
    except Exception as e2:
        return error_json_response(http_status=500, status='internal server error', msg=str(e2))


def setup_middlewares(app: "Application"):
    app.middlewares.append(error_handling_middleware)
    app.middlewares.append(validation_middleware)
