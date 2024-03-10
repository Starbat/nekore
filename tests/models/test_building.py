from decimal import Decimal
from typing import Final

from nekore.models import Apartment, Building, Tenant


def test_tenants(tenant_aurore_jones: Tenant, tenant_kim_jackson: Tenant) -> None:
    tenants: Final = (tenant_aurore_jones, tenant_kim_jackson)
    building: Final = Building(
        apartments=[Apartment(tenants=[t], floor_space=Decimal(100)) for t in tenants]
    )
    assert tuple(building.tenants) == tenants


def test_tenants_in(tenant_aurore_jones: Tenant, tenant_kim_jackson: Tenant) -> None:
    building: Final = Building(
        apartments=[
            Apartment(tenants=[t], floor_space=Decimal(100))
            for t in (tenant_aurore_jones, tenant_kim_jackson)
        ]
    )
    result: Final = building.tenants_in(tenant_aurore_jones.period)
    assert list(result) == [tenant_aurore_jones]
