from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/notes")
async def notes() -> JSONResponse:
    return JSONResponse({"status": "not_implemented"}, status_code=501)
