# WARNING
# This is intentionally vulnerable and must never be used in production.
# WARNING
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="/app/app/static"), name="static")


@app.get("/")
async def index() -> FileResponse:
    return FileResponse("/app/app/static/index.html")
