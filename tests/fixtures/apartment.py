from decimal import Decimal

import pytest

from nekore.models import Apartment, Tenant


@pytest.fixture
def apartment_1_of_building_a(
    tenant_kim_jackson: Tenant, tenant_aurore_jones: Tenant
) -> Apartment:
    return Apartment(
        name="1 of building A",
        floor_space=Decimal(100),
        tenants=(tenant_kim_jackson, tenant_aurore_jones),
    )


@pytest.fixture
def apartment_2_of_building_a(tenant_frank_maldonado: Tenant) -> Apartment:
    return Apartment(
        name="1 of building A",
        floor_space=Decimal(130),
        tenants=(tenant_frank_maldonado,),
    )
