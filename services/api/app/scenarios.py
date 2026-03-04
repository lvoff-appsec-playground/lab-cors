# WARNING
# This is intentionally vulnerable and must never be used in production.
# WARNING
from dataclasses import dataclass
from typing import List, Optional, Pattern


@dataclass(frozen=True)
class CorsScenario:
    name: str
    description: str

    reflect_origin: bool
    allow_null_origin: bool
    allow_credentials: bool

    allowlist_exact: Optional[List[str]]
    allowlist_regex: Optional[Pattern]
    allow_subdomains: bool

    set_vary_origin: bool

    allow_methods: List[str]
    allow_headers: List[str]
    max_age: int


LAB1_REFLECT_BASIC_ORIGIN = CorsScenario(
    name="lab1_reflect_basic_origin",
    description="Reflect any Origin and allow credentials.",
    reflect_origin=True,
    allow_null_origin=False,
    allow_credentials=True,
    allowlist_exact=None,
    allowlist_regex=None,
    allow_subdomains=False,
    set_vary_origin=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "X-Requested-With", "X-Api-Key", "X-Client-Version"],
    max_age=0,
)

LAB2_TRUSTED_NULL_ORIGIN = CorsScenario(
    name="lab2_trusted_null_origin",
    description="Allows Origin: null with credentials; no reflection for others.",
    reflect_origin=False,
    allow_null_origin=True,
    allow_credentials=True,
    allowlist_exact=None,
    allowlist_regex=None,
    allow_subdomains=False,
    set_vary_origin=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "X-Requested-With", "X-Api-Key", "X-Client-Version"],
    max_age=0,
)

ALLOW_ALL = CorsScenario(
    name="allow_all",
    description="Worst-case: reflect any origin, allow null, credentials, and all headers.",
    reflect_origin=True,
    allow_null_origin=True,
    allow_credentials=True,
    allowlist_exact=None,
    allowlist_regex=None,
    allow_subdomains=True,
    set_vary_origin=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "X-Requested-With", "X-Api-Key", "X-Client-Version"],
    max_age=0,
)

HARDENED = CorsScenario(
    name="hardened",
    description="Most restrictive: no reflection, no null, no credentials, no origins allowed.",
    reflect_origin=False,
    allow_null_origin=False,
    allow_credentials=False,
    allowlist_exact=[],
    allowlist_regex=None,
    allow_subdomains=False,
    set_vary_origin=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
    max_age=0,
)

SCENARIOS = {
    LAB1_REFLECT_BASIC_ORIGIN.name: LAB1_REFLECT_BASIC_ORIGIN,
    LAB2_TRUSTED_NULL_ORIGIN.name: LAB2_TRUSTED_NULL_ORIGIN,
    ALLOW_ALL.name: ALLOW_ALL,
    HARDENED.name: HARDENED,
}
