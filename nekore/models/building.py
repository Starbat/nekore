from dataclasses import dataclass, field
from typing import Collection, Final, Iterator

from .apartment import Apartment
from .tenant import Tenant
from .time_period import TimePeriod


@dataclass(frozen=True, slots=True)
class Building:
    name: str | None = None
    apartments: Collection[Apartment] = field(default_factory=tuple)

    @property
    def tenants(self) -> Iterator[Tenant]:
        """All tenants from all apartments."""
        return (t for a in self.apartments for t in a.tenants)

    def tenants_in(self, period: TimePeriod) -> Iterator[Tenant]:
        """
        Get all tenants of all apartments who occupied
        an apartment during that given period.
        """
        return (t for t in self.tenants if period.overlaps(t.period))

    def apartment_of(self, tenant: Tenant) -> Apartment:
        apartments: Final = (a for a in self.apartments if tenant in a.tenants)
        try:
            return next(apartments)
        except StopIteration:
            raise ValueError(f"{tenant} must be resident in an apartment of {self}.")
