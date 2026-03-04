import logging

from fastapi import FastAPI, Request
from starlette.responses import Response

from .config import load_settings
from .cors_engine import apply_cors_headers, build_cors_headers
from .logging_middleware import request_logging_middleware
from .scenarios import SCENARIOS, LAB1_REFLECT_BASIC_ORIGIN
from .routes import auth, me, transfer, notes, admin

logging.basicConfig(level=logging.INFO)

app = FastAPI()


def _is_preflight(request: Request) -> bool:
    return (
        request.method == "OPTIONS"
        and "origin" in request.headers
        and "access-control-request-method" in request.headers
    )


@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    return await request_logging_middleware(request, call_next)


@app.middleware("http")
async def cors_middleware(request: Request, call_next):
    settings = load_settings()
    scenario = SCENARIOS.get(settings.scenario_name, LAB1_REFLECT_BASIC_ORIGIN)

    if _is_preflight(request):
        response = Response(status_code=204)
        cors_headers = build_cors_headers(request, scenario, is_preflight=True)
        apply_cors_headers(response, cors_headers)
        return response

    response = await call_next(request)
    cors_headers = build_cors_headers(request, scenario, is_preflight=False)
    apply_cors_headers(response, cors_headers)
    return response


app.include_router(auth.router)
app.include_router(me.router)
app.include_router(transfer.router)
app.include_router(notes.router)
app.include_router(admin.router)
