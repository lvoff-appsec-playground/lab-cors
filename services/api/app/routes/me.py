from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/me")
async def me(request: Request) -> JSONResponse:
    sid = request.cookies.get("sid")
    if not sid:
        return JSONResponse({"error": "unauthorized"}, status_code=401)
    return JSONResponse({"user": "demo", "secret": "cors-lab-secret"})
