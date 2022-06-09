from dataclasses import dataclass
from decimal import Decimal
from typing import Any

from betriebskosten.building import Building
from betriebskosten.tenant import Tenant
from betriebskosten.time_period import TimePeriod


@dataclass(frozen=True, slots=True)
class ApartmentStrategy:
    name: str = "STK"

    def get_name(self) -> str:
        return self.name

    def total_shares(
        self,
        accounting_period: TimePeriod,
        building: Building,
    ) -> Decimal:
        return Decimal(len(building.apartments))

    def tenant_shares(
        self,
        accounting_period: TimePeriod,
        _: Any,
        tenant: Tenant,
    ) -> Decimal:
        use_days = Decimal(accounting_period.intersection(tenant.period).days)
        return use_days / accounting_period.duration.days
