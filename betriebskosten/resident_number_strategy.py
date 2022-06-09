from dataclasses import dataclass
from decimal import Decimal

from betriebskosten.building import Building
from betriebskosten.tenant import Tenant
from betriebskosten.time_period import TimePeriod


@dataclass(frozen=True, slots=True)
class ResidentNumberStrategy:
    name: str = "PNZ"

    def get_name(self) -> str:
        return self.name

    def total_shares(
        self,
        accounting_period: TimePeriod,
        building: Building,
    ) -> Decimal:
        total_person_days: Decimal = Decimal(0)
        for tenant in building.get_tenants():
            total_person_days += self._person_days(tenant, accounting_period)
        return total_person_days / accounting_period.duration.days

    def tenant_shares(
        self,
        accounting_period: TimePeriod,
        building: Building,
        tenant: Tenant,
    ) -> Decimal:
        person_days = self._person_days(tenant, accounting_period)
        return person_days / accounting_period.duration.days

    def _person_days(self, tenant: Tenant, accounting_period: TimePeriod) -> Decimal:
        use_days = tenant.period.intersection(accounting_period).days
        return Decimal(tenant.number_of_people * use_days)
