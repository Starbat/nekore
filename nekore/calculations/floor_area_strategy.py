from dataclasses import dataclass
from decimal import Decimal
from typing import Final

from nekore.models import Building, Tenant, TimePeriod


@dataclass(frozen=True, slots=True)
class FloorAreaStrategy:
    name: str = "NHN"

    def total_shares(self, _: TimePeriod, building: Building) -> Decimal:
        return Decimal(sum(a.floor_space for a in building.apartments))

    def tenant_shares(
        self, accounting_period: TimePeriod, building: Building, tenant: Tenant
    ) -> Decimal:
        apartment = building.apartment_of(tenant)
        days_of_use: Final = Decimal(tenant.time_of_use_in(accounting_period).days)
        time_share = days_of_use / accounting_period.duration.days
        return apartment.floor_space * time_share
