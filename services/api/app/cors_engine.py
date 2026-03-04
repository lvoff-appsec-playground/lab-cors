# WARNING
# This is intentionally vulnerable and must never be used in production.
# WARNING
from typing import Dict, Optional

from starlette.requests import Request
from starlette.responses import Response

from .scenarios import CorsScenario


def _origin_allowed(origin: Optional[str], scenario: CorsScenario) -> Optional[str]:
    if not origin:
        return None
    if origin == "null" and scenario.allow_null_origin:
        return origin
    if scenario.reflect_origin:
        return origin
    if scenario.allowlist_exact and origin in scenario.allowlist_exact:
        return origin
    if scenario.allowlist_regex and scenario.allowlist_regex.match(origin):
        return origin
    return None


def build_cors_headers(
    request: Request,
    scenario: CorsScenario,
    is_preflight: bool,
) -> Dict[str, str]:
    origin = request.headers.get("origin")
    allowed_origin = _origin_allowed(origin, scenario)
    if not allowed_origin:
        return {}

    headers: Dict[str, str] = {
        "Access-Control-Allow-Origin": allowed_origin,
    }

    if scenario.allow_credentials:
        headers["Access-Control-Allow-Credentials"] = "true"

    if scenario.set_vary_origin:
        headers["Vary"] = "Origin"

    if is_preflight:
        headers["Access-Control-Allow-Methods"] = ", ".join(scenario.allow_methods)
        headers["Access-Control-Allow-Headers"] = ", ".join(scenario.allow_headers)
        if scenario.max_age > 0:
            headers["Access-Control-Max-Age"] = str(scenario.max_age)

    return headers


def apply_cors_headers(response: Response, cors_headers: Dict[str, str]) -> None:
    if not cors_headers:
        return

    if "Vary" in cors_headers and "Vary" in response.headers:
        existing = response.headers.get("Vary", "")
        if "Origin" not in existing:
            response.headers["Vary"] = f"{existing}, Origin"
        cors_headers.pop("Vary", None)

    for key, value in cors_headers.items():
        response.headers[key] = value
