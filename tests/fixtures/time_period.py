from datetime import date
from typing import Final

import pytest

from nekore.models import TimePeriod


@pytest.fixture
def year_2020() -> TimePeriod:
    return TimePeriod(
        start=date(year=2020, month=1, day=1), end=date(year=2020, month=12, day=31)
    )


@pytest.fixture
def new_years_eve_2020() -> TimePeriod:
    new_years_eve: Final = date(year=2020, month=12, day=31)
    return TimePeriod(start=new_years_eve, end=new_years_eve)


@pytest.fixture
def nineties() -> TimePeriod:
    return TimePeriod(
        start=date(year=1990, month=1, day=1), end=date(year=1999, month=12, day=31)
    )
