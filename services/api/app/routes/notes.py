from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter()


@router.post("/notes")
async def notes(request: Request) -> JSONResponse:
    sid = request.cookies.get("sid")
    if not sid:
        return JSONResponse({"error": "unauthorized"}, status_code=401)

    content_type = request.headers.get("content-type", "")
    if "application/json" not in content_type:
        return JSONResponse({"error": "invalid_content_type"}, status_code=400)

    has_api_key = "x-api-key" in request.headers
    has_requested_with = "x-requested-with" in request.headers
    if not (has_api_key or has_requested_with):
        return JSONResponse({"error": "missing_required_header"}, status_code=400)

    try:
        payload = await request.json()
    except Exception:
        return JSONResponse({"error": "invalid_json"}, status_code=400)

    note = payload.get("note") if isinstance(payload, dict) else None
    if not isinstance(note, str):
        return JSONResponse({"error": "invalid_note"}, status_code=400)

    return JSONResponse({"status": "stored", "note": note}, status_code=201)
