import datetime as dt
from typing import Final

from nekore.models import Contact, TimePeriod
from nekore.models.tenant import Tenant, overlapping_in_time


def test_overlapping_in_time_with_all_overlapping() -> None:
    periods: Final = tuple(
        TimePeriod(
            start=dt.date.fromisoformat(start),
            end=dt.date.fromisoformat(end),
        )
        for start, end in (
            ("2020-01-01", "2020-01-10"),
            ("2020-01-02", "2020-01-11"),
            ("2020-01-03", "2020-01-12"),
        )
    )
    tenants: Final = tuple(
        Tenant(
            contact=Contact(f"Name{n}", f"Street{n}", str(n), f"1234{n}", f"City{n}"),
            number_of_people=n,
            period=p,
        )
        for n, p in enumerate(periods)
    )
    expected: Final = [
        (tenants[0], tenants[1]),
        (tenants[0], tenants[2]),
        (tenants[1], tenants[2]),
    ]
    assert list(overlapping_in_time(tenants)) == expected


def test_overlapping_in_time_with_no_overlapping() -> None:
    periods: Final = tuple(
        TimePeriod(
            start=dt.date.fromisoformat(start),
            end=dt.date.fromisoformat(end),
        )
        for start, end in (
            ("2020-01-01", "2020-01-03"),
            ("2020-01-04", "2020-01-06"),
            ("2020-01-07", "2020-01-09"),
        )
    )
    tenants: Final = tuple(
        Tenant(
            contact=Contact(f"Name{n}", f"Street{n}", str(n), f"1234{n}", f"City{n}"),
            number_of_people=n,
            period=p,
        )
        for n, p in enumerate(periods)
    )
    assert list(overlapping_in_time(tenants)) == []
