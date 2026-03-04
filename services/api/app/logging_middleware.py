# WARNING
# This is intentionally vulnerable and must never be used in production.
# WARNING
import json
import logging
from typing import Callable

from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger("corslab")


def _is_preflight(request: Request) -> bool:
    return (
        request.method == "OPTIONS"
        and "origin" in request.headers
        and "access-control-request-method" in request.headers
    )


async def request_logging_middleware(request: Request, call_next: Callable) -> Response:
    origin = request.headers.get("origin")
    has_cookie = "cookie" in request.headers
    preflight = _is_preflight(request)
    preflight_method = request.headers.get("access-control-request-method")
    preflight_headers = request.headers.get("access-control-request-headers")

    response = await call_next(request)

    log_entry = {
        "event": "preflight" if preflight else "request",
        "origin": origin,
        "method": request.method,
        "path": request.url.path,
        "has_cookie": has_cookie,
        "preflight": preflight,
        "preflight_method": preflight_method,
        "preflight_headers": preflight_headers,
        "cors_allow_origin": response.headers.get("access-control-allow-origin"),
        "cors_allow_credentials": response.headers.get("access-control-allow-credentials"),
        "cors_allow_methods": response.headers.get("access-control-allow-methods"),
        "cors_allow_headers": response.headers.get("access-control-allow-headers"),
    }

    logger.info(json.dumps(log_entry))
    return response
