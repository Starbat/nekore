from dataclasses import dataclass
from decimal import Decimal

from betriebskosten.building import Building
from betriebskosten.tenant import Tenant
from betriebskosten.time_period import TimePeriod


@dataclass(frozen=True, slots=True)
class ResidentNumberStrategy:
    name: str

    def total_shares(
        self,
        accounting_period: TimePeriod,
        building: Building,
    ) -> Decimal:
        person_days: int = 0
        for tenant in building.get_tenants():
            relevant_days = tenant.period.intersection(accounting_period).days
            person_days += tenant.number_of_people * relevant_days
        return Decimal(person_days)

    def tenant_shares(
        self,
        accounting_period: TimePeriod,
        building: Building,
        tenant: Tenant,
    ) -> Decimal:
        relevant_days = tenant.period.intersection(accounting_period).days
        return Decimal(tenant.number_of_people * relevant_days)
