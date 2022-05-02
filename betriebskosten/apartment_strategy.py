from dataclasses import dataclass
from decimal import Decimal
from typing import Any

from betriebskosten.building import Building
from betriebskosten.tenant import Tenant
from betriebskosten.time_period import TimePeriod


@dataclass(frozen=True)
class ApartmentStrategy:
    name: str

    def total_shares(
        self,
        accounting_period: TimePeriod,
        building: Building,
    ) -> Decimal:
        return Decimal(len(building.apartments) * accounting_period.duration.days)

    def tenant_shares(
        self,
        accounting_period: TimePeriod,
        _: Any,
        tenant: Tenant,
    ) -> Decimal:
        return Decimal(accounting_period.intersection(tenant.period).days)
