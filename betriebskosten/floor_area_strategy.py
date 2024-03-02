from dataclasses import dataclass
from decimal import Decimal

from .models import Apartment, Building, Tenant, TimePeriod


@dataclass(frozen=True, slots=True)
class FloorAreaStrategy:
    name: str = "NHN"

    def get_name(self) -> str:
        return self.name

    def total_shares(
        self,
        accounting_period: TimePeriod,
        building: Building,
    ) -> Decimal:
        return Decimal(sum(a.floor_space for a in building.apartments))

    def tenant_shares(
        self,
        accounting_period: TimePeriod,
        building: Building,
        tenant: Tenant,
    ) -> Decimal:
        apartment = self._get_tenant_apartment(building, tenant)
        use_days = Decimal(tenant.period.intersection(accounting_period).days)
        time_share = use_days / accounting_period.duration.days
        return apartment.floor_space * time_share

    def _get_tenant_apartment(self, building: Building, tenant: Tenant) -> Apartment:
        for apartment in building.apartments:
            if tenant in apartment.tenants:
                return apartment
        raise ValueError(f"{tenant} must be resident in an apartment of {building}.")
