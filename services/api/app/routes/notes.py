# Educational purpose:
# --------------------
# This endpoint is intentionally designed as an "API-style" state-changing endpoint.
#
# It requires:
#   - application/json content type
#   - at least one custom header (X-Api-Key or X-Requested-With)
#
# Why?
#   1) To force the request to be a non-simple CORS request.
#      This triggers a browser preflight (OPTIONS) request.
#
#   2) To prevent execution via a plain HTML <form> submission,
#      since forms cannot set arbitrary custom headers.
#
# This allows the lab to demonstrate:
#   - How preflight works
#   - How Access-Control-Allow-Headers and Allow-Methods affect execution
#   - The difference between "request sent" and "response readable"
#   - Why CORS misconfiguration can allow cross-origin API abuse


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

    # Force preflight request
    # since it's a non-simple request (uses custom headers)
    has_api_key = "x-api-key" in request.headers
    has_requested_with = "x-requested-with" in request.headers
    if not (has_api_key or has_requested_with):
        return JSONResponse({"error": "missing_ajax_header_or_api_key"}, status_code=400)

    try:
        payload = await request.json()
    except Exception:
        return JSONResponse({"error": "invalid_json"}, status_code=400)

    note = payload.get("note") if isinstance(payload, dict) else None
    if not isinstance(note, str):
        return JSONResponse({"error": "invalid_note"}, status_code=400)

    return JSONResponse({"status": "stored", "note": note}, status_code=201)
