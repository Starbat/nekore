from decimal import Decimal

import pytest

from betriebskosten.models.allocation_strategy import AllocationStrategy
from betriebskosten.models.building import Building
from betriebskosten.models.tenant import Tenant
from betriebskosten.models.time_period import TimePeriod


class DummyAllocationStrategy:
    def get_name(self) -> str:
        return "dummy name"

    def total_shares(
        self, accounting_period: TimePeriod, building: Building
    ) -> Decimal:
        raise NotImplementedError

    def tenant_shares(
        self, accounting_period: TimePeriod, building: Building, tenant: Tenant
    ) -> Decimal:
        raise NotImplementedError


@pytest.fixture
def dummy_allocation_strategy() -> AllocationStrategy:
    return DummyAllocationStrategy()
