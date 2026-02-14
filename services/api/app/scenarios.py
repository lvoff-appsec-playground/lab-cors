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
    allow_headers=["Content-Type", "X-Requested-With", "X-Api-Key"],
    max_age=0,
)

SCENARIOS = {
    LAB1_REFLECT_BASIC_ORIGIN.name: LAB1_REFLECT_BASIC_ORIGIN,
}
