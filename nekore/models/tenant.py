from dataclasses import dataclass
from datetime import timedelta
from decimal import Decimal
from itertools import combinations
from typing import Final, Iterable, Iterator

from .contact import Contact
from .time_period import TimePeriod


@dataclass(frozen=True, slots=True)
class Tenant:
    contact: Contact
    number_of_people: int
    period: TimePeriod
    prepaid: Decimal = Decimal(0)

    def time_of_use_in(self, period: TimePeriod) -> timedelta:
        use_time: Final = self.period.intersection(period)
        if use_time is None:
            return timedelta(0)
        return use_time.duration


def overlapping_in_time(tenants: Iterable[Tenant]) -> Iterator[tuple[Tenant, Tenant]]:
    tenant_pairs: Final = combinations(tenants, 2)
    return filter(lambda t: t[0].period.overlaps(t[1].period), tenant_pairs)
