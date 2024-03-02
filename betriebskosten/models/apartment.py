from dataclasses import dataclass, field
from decimal import Decimal

from .tenant import Tenant


@dataclass(frozen=True, eq=True, slots=True)
class Apartment:
    floor_space: Decimal
    name: str | None = None
    tenants: list[Tenant] = field(default_factory=list, compare=False)

    def __post_init__(self) -> None:
        self._validate_tenant_periods()

    def _validate_tenant_periods(self) -> None:
        for t1 in self.tenants:
            for t2 in self.tenants:
                if t1 is not t2 and t1.period.intersection(t2.period):
                    raise ValueError(f"{t1} and {t2} have overlapping periods.")
