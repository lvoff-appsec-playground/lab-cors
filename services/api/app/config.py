import os
from dataclasses import asdict, dataclass
from typing import Any, Dict


@dataclass(frozen=True)
class Settings:
    scenario_name: str
    cookie_samesite: str
    cookie_secure: bool
    cookie_httponly: bool
    cookie_domain: str
    cookie_path: str


def _to_bool(value: str, default: bool) -> bool:
    if value is None:
        return default
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    elif normalized in {"0", "false", "no", "off"}:
        return False
    return default


def _coerce_bool(value: Any, default: bool) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return _to_bool(value, default)
    return bool(value)


_runtime_overrides: Dict[str, Any] = {}


def load_settings() -> Settings:
    scenario_name = os.getenv("SCENARIO", "lab1_reflect_basic_origin")
    cookie_samesite = os.getenv("COOKIE_SAMESITE", "None")
    cookie_secure = _to_bool(os.getenv("COOKIE_SECURE"), False)
    cookie_httponly = _to_bool(os.getenv("COOKIE_HTTPONLY"), True)
    cookie_domain = os.getenv("COOKIE_DOMAIN", "api.local")
    cookie_path = os.getenv("COOKIE_PATH", "/")

    if "scenario_name" in _runtime_overrides:
        scenario_name = str(_runtime_overrides["scenario_name"])
    if "cookie_samesite" in _runtime_overrides:
        cookie_samesite = str(_runtime_overrides["cookie_samesite"])
    if "cookie_secure" in _runtime_overrides:
        cookie_secure = _coerce_bool(_runtime_overrides["cookie_secure"], cookie_secure)
    if "cookie_httponly" in _runtime_overrides:
        cookie_httponly = _coerce_bool(_runtime_overrides["cookie_httponly"], cookie_httponly)
    if "cookie_domain" in _runtime_overrides:
        cookie_domain = str(_runtime_overrides["cookie_domain"])
    if "cookie_path" in _runtime_overrides:
        cookie_path = str(_runtime_overrides["cookie_path"])

    return Settings(
        scenario_name=scenario_name,
        cookie_samesite=cookie_samesite,
        cookie_secure=cookie_secure,
        cookie_httponly=cookie_httponly,
        cookie_domain=cookie_domain,
        cookie_path=cookie_path,
    )


def update_settings(updates: Dict[str, Any]) -> Settings:
    _runtime_overrides.update(updates)
    return load_settings()


def settings_to_dict(settings: Settings) -> Dict[str, Any]:
    return asdict(settings)
