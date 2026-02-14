import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    scenario_name: str
    cookie_samesite: str
    cookie_secure: bool
    cookie_domain: str
    cookie_path: str


def _to_bool(value: str, default: bool) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def load_settings() -> Settings:
    return Settings(
        scenario_name=os.getenv("SCENARIO", "lab1_reflect_basic_origin"),
        cookie_samesite=os.getenv("COOKIE_SAMESITE", "None"),
        cookie_secure=_to_bool(os.getenv("COOKIE_SECURE"), False),
        cookie_domain=os.getenv("COOKIE_DOMAIN", "api.local"),
        cookie_path=os.getenv("COOKIE_PATH", "/"),
    )
