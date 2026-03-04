# WARNING
# This is intentionally vulnerable and must never be used in production.
# WARNING

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter()



# Educational purpose:
# --------------------
# This endpoint returns sensitive profile information about the
# currently authenticated user (based on the "sid" cookie).
#
# Behavior:
#   1) If a valid "sid" cookie is present:
#        → return user profile data (e.g., username, email, role, balance)
#   2) If no "sid" cookie is present:
#        → return 401 Unauthorized
#
# Why?:
#   This endpoint is intentionally designed to demonstrate how
#   sensitive data can be exposed via a simple GET request when:
#       - Cookies are automatically included in cross-origin requests
#       - SameSite allows cross-site cookie transmission
#       - CORS is misconfigured (e.g., origin reflection + credentials)
#
# This endpoint allows the lab to demonstrate:
#   - Show how misconfigured CORS enables cross-origin data exfiltration
#   - Demonstrate that GET endpoints are common targets for data theft
#   - Reinforce that CORS protects *read access* in the browser,
#     not whether the request is sent
#   - Illustrate the importance of strict origin allowlists
#
# In a vulnerable configuration, an attacker page can execute:
#   fetch("http://api.local/me", { credentials: "include" })
# and directly read the victim's private information.
#
# This endpoint models a common real-world API mistake:
#   Sensitive data exposed via GET + cookie-based auth + permissive CORS
#   (Access-Control-Allow-Origin and Access-Control-Allow-Credentials usage)

@router.get("/me")
async def me(request: Request) -> JSONResponse:
    sid = request.cookies.get("sid")
    if not sid:
        return JSONResponse({"error": "unauthorized"}, status_code=401)
    return JSONResponse({"user": "user1", "secret": "cors-lab-secret"})
