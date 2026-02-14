from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()


@router.post("/transfer")
async def transfer() -> JSONResponse:
    return JSONResponse({"status": "not_implemented"}, status_code=501)
