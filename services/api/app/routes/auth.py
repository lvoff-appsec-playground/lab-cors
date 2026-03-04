# WARNING
# This is intentionally vulnerable and must never be used in production.
# WARNING
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from ..cookie_policy import build_cookie_params
from ..config import load_settings

router = APIRouter()


@router.get("/login")
async def login() -> JSONResponse:
    settings = load_settings()
    response = JSONResponse({"status": "ok", "user": "demo"})
    cookie_params = build_cookie_params(settings)
    response.set_cookie("sid", "user1", **cookie_params)
    return response
