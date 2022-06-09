import datetime as dt
from decimal import Decimal

from betriebskosten import Apartment, Contact, Tenant, TimePeriod


def test_validate_tenant_periods() -> None:
    t1 = Tenant(
        contact=Contact("Tenant 1", "Street", "1", "12345", "city"),
        number_of_people=1,
        period=TimePeriod(
            start=dt.date.fromisoformat("2020-01-01"),
            end=dt.date.fromisoformat("2020-01-10"),
        ),
    )
    t2 = Tenant(
        contact=Contact("Tenant 1", "Street", "1", "12345", "city"),
        number_of_people=1,
        period=TimePeriod(
            start=dt.date.fromisoformat("2020-02-01"),
            end=dt.date.fromisoformat("2020-02-10"),
        ),
    )
    Apartment(floor_space=Decimal(50), tenants=[t1, t2])
