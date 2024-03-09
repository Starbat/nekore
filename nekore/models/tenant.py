from dataclasses import dataclass
from decimal import Decimal

from .contact import Contact
from .time_period import TimePeriod


@dataclass(frozen=True, slots=True)
class Tenant:
    contact: Contact
    number_of_people: int
    period: TimePeriod
    prepaid: Decimal = Decimal(0)
