import pytest

from nekore.models import Contact, Tenant, TimePeriod


@pytest.fixture
def tenant_aurore_jones(aurore_jones: Contact, year_2020: TimePeriod) -> Tenant:
    return Tenant(contact=aurore_jones, number_of_people=1, period=year_2020)


@pytest.fixture
def tenant_kim_jackson(kim_jackson: Contact, nineties: TimePeriod) -> Tenant:
    return Tenant(contact=kim_jackson, number_of_people=1, period=nineties)


@pytest.fixture
def tenant_frank_maldonado(frank_maldonado: Contact, year_2020: TimePeriod) -> Tenant:
    return Tenant(contact=frank_maldonado, number_of_people=2, period=year_2020)
