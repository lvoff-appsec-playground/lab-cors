from typing import Dict

from .config import Settings


def build_cookie_params(settings: Settings) -> Dict[str, object]:
    return {
        "httponly": True,
        "samesite": settings.cookie_samesite,
        "secure": settings.cookie_secure,
        "domain": settings.cookie_domain,
        "path": settings.cookie_path,
    }
