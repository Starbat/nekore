from datetime import date
from decimal import Decimal

import pytest

from nekore.models import Invoice


@pytest.fixture
def privileged_invoice() -> Invoice:
    return Invoice(
        "privileged invoice issuer name",
        net_amount=Decimal(100),
        date=date(year=2020, month=1, day=1),
        gross_amount=Decimal(150),
        privileged_amount=Decimal(10),
        name="privileged invoice",
    )


@pytest.fixture
def unprivileged_invoice() -> Invoice:
    return Invoice(
        "unprivileged invoice issuer name",
        net_amount=Decimal(100),
        date=date(year=2020, month=1, day=1),
        gross_amount=Decimal(150),
        privileged_amount=Decimal(0),
        name="unprivileged invoice",
    )
