from dataclasses import dataclass
from decimal import Decimal
from typing import Any

from nekore.models import Building, Tenant, TimePeriod


@dataclass(frozen=True, slots=True)
class ApartmentStrategy:
    name: str = "STK"

    def total_shares(self, _: TimePeriod, building: Building) -> Decimal:
        return Decimal(len(building.apartments))

    def tenant_shares(
        self, accounting_period: TimePeriod, _: Any, tenant: Tenant
    ) -> Decimal:
        days_of_use = Decimal(tenant.time_of_use_in(accounting_period).days)
        return days_of_use / accounting_period.duration.days
