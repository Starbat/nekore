from decimal import Decimal

import pytest

from nekore.models import AllocationStrategy, Building, Tenant, TimePeriod


class DummyAllocationStrategy:
    @property
    def name(self) -> str:
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
