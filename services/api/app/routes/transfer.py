# This is intentionally vulnerable and must never be used in production.

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse

from ..db.transfer_db import record_transfer

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

    transfer_id = record_transfer(user_from="user1", user_to=str(to), amount=str(amount))

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
# Why?
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

    transfer_id = record_transfer(user_from="user1", user_to=str(to), amount=str(amount))

    return JSONResponse({
        "status": "transfer_completed",
        "transfer_id": transfer_id,
        "to": to,
        "amount": amount
    })
