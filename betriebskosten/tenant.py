from dataclasses import dataclass
from decimal import Decimal

from betriebskosten.contact import Contact
from betriebskosten.time_period import TimePeriod


@dataclass(frozen=True, slots=True)
class Tenant:
    contact: Contact
    number_of_people: int
    period: TimePeriod
    prepaid: Decimal = Decimal(0)
