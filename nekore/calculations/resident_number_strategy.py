from dataclasses import dataclass
from decimal import Decimal
from typing import Final

from nekore.models import Building, Tenant, TimePeriod


@dataclass(frozen=True, slots=True)
class ResidentNumberStrategy:
    name: str = "PNZ"

    def get_name(self) -> str:
        return self.name

    def total_shares(
        self, accounting_period: TimePeriod, building: Building
    ) -> Decimal:
        total_person_days: Decimal = Decimal(0)
        for tenant in building.tenants_in(accounting_period):
            total_person_days += self._person_days(tenant, accounting_period)
        return total_person_days / accounting_period.duration.days

    def tenant_shares(
        self, accounting_period: TimePeriod, _: Building, tenant: Tenant
    ) -> Decimal:
        person_days = self._person_days(tenant, accounting_period)
        return person_days / accounting_period.duration.days

    def _person_days(self, tenant: Tenant, accounting_period: TimePeriod) -> Decimal:
        days_of_use: Final = Decimal(tenant.time_of_use_in(accounting_period).days)
        return Decimal(tenant.number_of_people * days_of_use)
