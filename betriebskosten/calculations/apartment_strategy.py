from dataclasses import dataclass
from decimal import Decimal
from typing import Any

from betriebskosten.models import Building, Tenant, TimePeriod


@dataclass(frozen=True, slots=True)
class ApartmentStrategy:
    name: str = "STK"

    def get_name(self) -> str:
        return self.name

    def total_shares(self, _: TimePeriod, building: Building) -> Decimal:
        return Decimal(len(building.apartments))

    def tenant_shares(
        self, accounting_period: TimePeriod, _: Any, tenant: Tenant
    ) -> Decimal:
        use_days = Decimal(accounting_period.intersection(tenant.period).days)
        return use_days / accounting_period.duration.days
