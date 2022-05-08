from dataclasses import dataclass
from decimal import Decimal

from betriebskosten.apartment import Apartment
from betriebskosten.building import Building
from betriebskosten.tenant import Tenant
from betriebskosten.time_period import TimePeriod


@dataclass(frozen=True, slots=True)
class FloorAreaStrategy:
    name: str

    def total_shares(
        self,
        accounting_period: TimePeriod,
        building: Building,
    ) -> Decimal:
        return Decimal(
            sum(a.floor_space for a in building.apartments)
            * accounting_period.duration.days
        )

    def tenant_shares(
        self,
        accounting_period: TimePeriod,
        building: Building,
        tenant: Tenant,
    ) -> Decimal:
        apartment = self._get_tenant_apartment(building, tenant)
        accounting_days = tenant.period.intersection(accounting_period).days
        return apartment.floor_space * accounting_days

    def _get_tenant_apartment(self, building: Building, tenant: Tenant) -> Apartment:
        for apartment in building.apartments:
            if tenant in apartment.tenants:
                return apartment
        raise ValueError(f"{tenant} must be resident in an apartment of {building}.")
