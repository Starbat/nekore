from dataclasses import dataclass, field
from decimal import Decimal
from typing import Collection

from .tenant import Tenant, overlapping_in_time


@dataclass(frozen=True, eq=True, slots=True)
class Apartment:
    floor_space: Decimal
    name: str | None = None
    tenants: Collection[Tenant] = field(default_factory=tuple, compare=False)

    def __post_init__(self) -> None:
        self._validate_tenant_periods()

    def _validate_tenant_periods(self) -> None:
        first = next(overlapping_in_time(self.tenants), None)
        if first:
            raise ValueError(f"{first[0]} and {first[1]} have overlapping periods.")
