from dataclasses import dataclass, field
from typing import Iterator

from .apartment import Apartment
from .tenant import Tenant
from .time_period import TimePeriod


@dataclass(frozen=True, slots=True)
class Building:
    name: str | None = None
    apartments: list[Apartment] = field(default_factory=list)

    def get_tenants(self, period: TimePeriod | None = None) -> Iterator[Tenant]:
        """
        Get all tenants of all apartments.
        If a period is passed as an argument, only tenants who occupied
        an apartment during that period are returned.
        """
        return (
            t
            for a in self.apartments
            for t in a.tenants
            if period is None or period.intersection(t.period).days > 0
        )

    def get_apartment(self, tenant: Tenant) -> Apartment:
        apartments = [a for a in self.apartments if tenant in a.tenants]
        if len(apartments) != 1:
            raise NotImplementedError
        return apartments[0]
