from decimal import Decimal
from typing import Protocol

from .building import Building
from .tenant import Tenant
from .time_period import TimePeriod


class AllocationStrategy(Protocol):
    """
    A class which calculates how costs are allocated among tenants.
    """

    @property
    def name(self) -> str: ...

    def total_shares(
        self, accounting_period: TimePeriod, building: Building
    ) -> Decimal: ...

    def tenant_shares(
        self, accounting_period: TimePeriod, building: Building, tenant: Tenant
    ) -> Decimal: ...
