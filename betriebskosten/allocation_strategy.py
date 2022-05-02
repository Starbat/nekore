from decimal import Decimal
from typing import Protocol

from betriebskosten.building import Building
from betriebskosten.tenant import Tenant
from betriebskosten.time_period import TimePeriod


class AllocationStrategy(Protocol):
    """
    A class which calculates how costs are allocated among tenants.
    """

    def total_shares(
        self,
        accounting_period: TimePeriod,
        building: Building,
    ) -> Decimal:
        ...

    def tenant_shares(
        self,
        accounting_period: TimePeriod,
        building: Building,
        tenant: Tenant,
    ) -> Decimal:
        ...
