from dataclasses import dataclass
from decimal import Decimal
from typing import Final

from nekore.models import Building, Tenant, TimePeriod


@dataclass(frozen=True, slots=True)
class ResidentNumberStrategy:
    name: str = "PNZ"

    def total_shares(
        self, accounting_period: TimePeriod, building: Building
    ) -> Decimal:
        tenants: Final = building.tenants
        total_person_days = sum(person_days(t, accounting_period) for t in tenants)
        return Decimal(total_person_days) / accounting_period.duration.days

    def tenant_shares(
        self, accounting_period: TimePeriod, _: Building, tenant: Tenant
    ) -> Decimal:
        _person_days: Final = Decimal(person_days(tenant, accounting_period))
        return _person_days / accounting_period.duration.days


def person_days(tenant: Tenant, accounting_period: TimePeriod) -> int:
    days_of_use: Final = tenant.time_of_use_in(accounting_period).days
    return tenant.number_of_people * days_of_use
