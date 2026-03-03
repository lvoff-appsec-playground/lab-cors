# WARNING
# This is intentionally vulnerable and must never be used in production.
# WARNING

from fastapi import APIRouter, Header, Request
from fastapi.responses import HTMLResponse, JSONResponse

from ..db.transfer_db import (
    latest_transfer_id_by_user,
    list_transfers_by_user,
    record_transfer,
)

router = APIRouter()


@router.get("/transfer")
async def transfer_form() -> HTMLResponse:
    # Educational case: this form demonstrates a simple POST that would be
    # "simple request" eligible. Keep it visible so the user can see the form.
    html = """
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <title>Transfer</title>
      </head>
      <body>
        <h1>Transfer</h1>
        <form action="/transfer" method="POST">
          <label>
            To:
            <input type="text" name="to" value="me">
          </label>
          <br>
          <label>
            Amount:
            <input type="text" name="amount" value="1000">
          </label>
          <br>
          <button type="submit">Submit transfer</button>
        </form>
      </body>
    </html>
    """
    return HTMLResponse(content=html)



# Educational purpose:
# --------------------
# This endpoint is intentionally designed as a classic web-style
# state-changing action (e.g., money transfer).
#
# It accepts simple form submissions (application/x-www-form-urlencoded)
# and does NOT require custom headers.
#
# Why?
#   1) To allow execution via a cross-origin HTML <form>.
#      This makes it a "simple request" (no preflight).
#
#   2) To demonstrate that CORS does NOT prevent state-changing requests.
#      Even if the browser blocks reading the response,
#      the request may still be sent and processed.
#
# This allows the lab to demonstrate:
#   - CORS vs CSRF distinction
#   - The impact of SameSite cookie settings
#   - The difference between "request execution" and "response visibility"
@router.post("/transfer")
async def transfer(request: Request) -> JSONResponse:
    sid = request.cookies.get("sid")
    if not sid:
        return JSONResponse({"error": "unauthorized"}, status_code=401)

    form = await request.form()
    to = form.get("to")
    amount = form.get("amount")

    if not to or not amount:
        return JSONResponse({"error": "invalid_transfer"}, status_code=400)

    transfer_id = record_transfer(user_from=sid, user_to=str(to), amount=str(amount))

    return JSONResponse({
        "status": "transfer_completed",
        "transfer_id": transfer_id,
        "to": to,
        "amount": amount
    })



# Educational purpose:
# --------------------
# This endpoint intentionally implements a state-changing action using GET,
# which is a deliberately insecure and outdated design pattern.
#
# Why?:
#   1) To demonstrate why state-changing operations must never use GET.
#      GET requests are automatically triggered by:
#         - <img>
#         - <script>
#         - <iframe>
#         - <a> links
#      and therefore can be abused without JavaScript.
#
#   2) To show that CORS is irrelevant in this case.
#      CORS only governs whether JavaScript can read responses —
#      it does NOT prevent the browser from sending cross-origin GET requests.
#
#   3) To highlight that CSRF protections (e.g., SameSite cookies, CSRF tokens)
#      are required to defend state-changing endpoints.
#
# This endpoint allows the lab to demonstrate:
#   - How simple cross-origin GET requests bypass CORS restrictions
#   - Why "safe methods" (GET) must not change state
#   - The importance of proper HTTP method semantics
#   - The interaction between SameSite cookies and navigation requests

@router.get("/transfer-legacy")
async def transfer_legacy(request: Request) -> JSONResponse:
    sid = request.cookies.get("sid")
    if not sid:
        return JSONResponse({"error": "unauthorized"}, status_code=401)

    to = request.query_params.get("to")
    amount = request.query_params.get("amount")

    if not to or not amount:
        return JSONResponse({"error": "invalid_transfer"}, status_code=400)

    transfer_id = record_transfer(user_from=sid, user_to=str(to), amount=str(amount))

    return JSONResponse({
        "status": "transfer_completed",
        "transfer_id": transfer_id,
        "to": to,
        "amount": amount
    })



# Educational purpose:
# --------------------
# This endpoint returns all transfers associated with the currently
# authenticated user (based on the "sid" cookie).
#
# Behavior:
#   1) If a valid "sid" cookie is present:
#        → return only transfers where user_from == sid
#   2) If no "sid" cookie is present:
#        → return an empty list
#
# Why?:
#   This endpoint is intentionally designed to demonstrate how
#   sensitive data can be exposed via a simple GET request when:
#       - Cookies are automatically included (credentials: include)
#       - SameSite allows cross-site cookie sending
#       - CORS is misconfigured (e.g., origin reflection + credentials)
#
# This endpoint allows the lab to demonstrate:
#   - Show that GET endpoints can leak sensitive information
#   - Demonstrate that CORS controls *read access*, not request execution
#   - Highlight that credentialed cross-origin requests can expose private data
#   - Reinforce the difference between:
#         "Request sent" vs "Response readable"
#
# In a vulnerable CORS configuration, an attacker page can:
#   fetch("http://api.local/transfers", { credentials: "include" })
# and read the victim's transfer history.
#
# This endpoint models a common real-world API mistake:
#   Sensitive data exposed via GET + cookie-based auth + permissive CORS
#   (Access-Control-Allow-Origin and Access-Control-Allow-Credentials usage)

@router.get("/transfers")
async def list_transfers(request: Request, x_client_version: str | None = Header(None)) -> JSONResponse:
    # Force preflight request
    # since it's a non-simple request (uses custom headers)
    # Option 1
    if x_client_version != "1":
        return JSONResponse({"error": "missing_ajax_header_or_api_key"}, status_code=400)
    # Option 2
    has_api_key = "x-api-key" in request.headers
    has_requested_with = "x-requested-with" in request.headers
    if not (has_api_key or has_requested_with):
        return JSONResponse({"error": "missing_ajax_header_or_api_key"}, status_code=400)

    sid = request.cookies.get("sid")
    if not sid:
        return JSONResponse({"transfers": []})

    transfers = list_transfers_by_user(sid)
    return JSONResponse({"transfers": transfers})



# Educational purpose:
# --------------------
# /account-meta demonstrates an advanced CORS nuance:
# "response headers are NOT automatically readable by cross-origin JavaScript."
#
# This endpoint intentionally leaks sensitive metadata via custom response headers
# (e.g., X-Account-Tier, X-Last-Transfer-Id).
#
# This endpoint allows the lab to demonstrate:
#   - Even if CORS allows reading the response body, browsers only expose a small
#     set of "simple response headers" to JS by default.
#   - To allow JS to read custom headers cross-origin, the server must explicitly set:
#       Access-Control-Expose-Headers: X-Account-Tier, X-Last-Transfer-Id
#
# This lab allows you to compare:
#   - CORS misconfig that allows reading BODY (classic)
#   - CORS misconfig that additionally exposes sensitive HEADERS (advanced)

@router.get("/account-meta")
async def account_meta(request: Request) -> JSONResponse:
    sid = request.cookies.get("sid")
    if not sid:
        return JSONResponse({"error": "unauthorized"}, status_code=401)

    last_transfer_id = latest_transfer_id_by_user(sid)
    headers = {
        "X-Account-Tier": "gold" if sid == "user1" else "free",
        "X-Last-Transfer-Id": "" if last_transfer_id is None else str(last_transfer_id),
        "X-Internal-User-Id": sid,
    }
    return JSONResponse({"status": "ok"}, headers=headers)
