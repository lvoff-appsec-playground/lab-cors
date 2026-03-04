import json

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, ConfigDict

from ..config import load_settings, settings_to_dict, update_settings
from ..db.transfer_db import list_all_transfers
from ..scenarios import SCENARIOS

router = APIRouter()


class ConfigUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    scenario_name: str | None = None
    cookie_samesite: str | None = None
    cookie_secure: bool | str | None = None
    cookie_httponly: bool | str | None = None
    cookie_domain: str | None = None
    cookie_path: str | None = None


@router.get("/admin/transfers")
async def admin_transfers(request: Request) -> JSONResponse:
    sid = request.cookies.get("sid")
    if sid != "admin":
        return JSONResponse({"error": "unauthorized"}, status_code=401)

    transfers = list_all_transfers()
    return JSONResponse({"transfers": transfers})


@router.post("/admin/config")
async def admin_config(request: Request, payload: ConfigUpdate) -> JSONResponse:
    sid = request.cookies.get("sid")
    if sid != "admin":
        return JSONResponse({"error": "unauthorized"}, status_code=401)

    updates = payload.model_dump(exclude_unset=True, exclude_none=True)
    scenario_name = updates.get("scenario_name")
    if scenario_name is not None and scenario_name not in SCENARIOS:
        return JSONResponse({"error": "invalid_scenario"}, status_code=400)

    settings = update_settings(updates)
    return JSONResponse({"status": "ok", "settings": settings_to_dict(settings)})


@router.get("/admin/config")
async def admin_config_page(request: Request) -> HTMLResponse:
    sid = request.cookies.get("sid")
    if sid != "admin":
        return HTMLResponse("<h1>Unauthorized</h1>", status_code=401)

    settings = settings_to_dict(load_settings())
    settings_json = json.dumps(settings)
    scenario_options = "\n".join(
        f'<option value="{name}">{name}</option>' for name in SCENARIOS.keys()
    )
    cookie_samesite_options = "\n".join(
        f'<option value="{value}">{value}</option>' for value in ["None", "Lax", "Strict"]
    )

    html = f"""
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <title>Admin Config</title>
        <style>
          body {{ font-family: Arial, sans-serif; margin: 24px; }}
          label {{ display: block; margin: 8px 0 4px; }}
          input, select {{ padding: 6px; min-width: 280px; }}
          button {{ margin-top: 12px; padding: 8px 12px; }}
          pre {{ background: #f4f4f4; padding: 12px; }}
        </style>
      </head>
      <body>
        <h1>Admin Config</h1>
        <p>Current settings are prefilled. Submit to apply runtime overrides.</p>

        <form id="config-form">
          <label for="scenario_name">Scenario</label>
          <select id="scenario_name" name="scenario_name">
            {scenario_options}
          </select>

          <label for="cookie_samesite">Cookie SameSite</label>
          <select id="cookie_samesite" name="cookie_samesite">
            {cookie_samesite_options}
          </select>

          <label for="cookie_secure">Cookie Secure</label>
          <select id="cookie_secure" name="cookie_secure">
            <option value="true">true</option>
            <option value="false">false</option>
          </select>

          <label for="cookie_httponly">Cookie HttpOnly</label>
          <select id="cookie_httponly" name="cookie_httponly">
            <option value="true">true</option>
            <option value="false">false</option>
          </select>

          <label for="cookie_domain">Cookie Domain</label>
          <input id="cookie_domain" name="cookie_domain" type="text">

          <label for="cookie_path">Cookie Path</label>
          <input id="cookie_path" name="cookie_path" type="text">

          <button type="button" id="apply-button">Apply</button>
        </form>

        <h2>Result</h2>
        <pre id="output">(no output yet)</pre>

        <script>
          const current = {settings_json};
          document.getElementById("scenario_name").value = current.scenario_name;
          document.getElementById("cookie_samesite").value = current.cookie_samesite;
          document.getElementById("cookie_secure").value = String(current.cookie_secure);
          document.getElementById("cookie_httponly").value = String(current.cookie_httponly);
          document.getElementById("cookie_domain").value = current.cookie_domain;
          document.getElementById("cookie_path").value = current.cookie_path;

          const output = document.getElementById("output");
          document.getElementById("apply-button").addEventListener("click", async () => {{
            output.textContent = "Submitting...";
            const payload = {{
              scenario_name: document.getElementById("scenario_name").value,
              cookie_samesite: document.getElementById("cookie_samesite").value,
              cookie_secure: document.getElementById("cookie_secure").value,
              cookie_httponly: document.getElementById("cookie_httponly").value,
              cookie_domain: document.getElementById("cookie_domain").value,
              cookie_path: document.getElementById("cookie_path").value,
            }};
            try {{
              const response = await fetch("/admin/config", {{
                method: "POST",
                headers: {{
                  "Content-Type": "application/json",
                }},
                credentials: "include",
                body: JSON.stringify(payload),
              }});
              let data = null;
              try {{
                data = await response.json();
              }} catch (_) {{
                const text = await response.text();
                output.textContent = `Status: ${{response.status}}\\n${{text}}`;
                return;
              }}
              output.textContent = `Status: ${{response.status}}\\n${{JSON.stringify(data, null, 2)}}`;
              if (response.ok && data.settings) {{
                const updated = data.settings;
                document.getElementById("scenario_name").value = updated.scenario_name;
                document.getElementById("cookie_samesite").value = updated.cookie_samesite;
                document.getElementById("cookie_secure").value = String(updated.cookie_secure);
                document.getElementById("cookie_httponly").value = String(updated.cookie_httponly);
                document.getElementById("cookie_domain").value = updated.cookie_domain;
                document.getElementById("cookie_path").value = updated.cookie_path;
              }}
            }} catch (error) {{
              output.textContent = `Error: ${{error}}`;
            }}
          }});
        </script>
      </body>
    </html>
    """
    return HTMLResponse(html)
