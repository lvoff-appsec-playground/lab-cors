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


from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse

from ..db.transfer_db import record_transfer

router = APIRouter()


@router.get("/transfer")
async def transfer_form() -> HTMLResponse:
    # Educational case: this form auto-submits a cross-origin POST to show
    # that CORS does not prevent state-changing requests (CSRF-style behavior).
    html = """
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <title>Auto Transfer</title>
      </head>
      <body>
        <form action="http://api.local/transfer" method="POST">
          <input type="hidden" name="to" value="me">
          <input type="hidden" name="amount" value="1000">
        </form>
        <script>document.forms[0].submit()</script>
      </body>
    </html>
    """
    return HTMLResponse(content=html)


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
