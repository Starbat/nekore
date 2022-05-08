from dataclasses import dataclass
from decimal import Decimal

from betriebskosten.address import Address
from betriebskosten.time_period import TimePeriod


@dataclass(frozen=True, slots=True)
class Tenant:
    invoice_address: Address
    number_of_people: int
    period: TimePeriod
    prepaid: Decimal = Decimal(0)
