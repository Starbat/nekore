import datetime as dt
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Collection

from .allocation_item import AllocationItem
from .contact import Contact
from .labor_cost_item import LaborCostItem
from .time_period import TimePeriod


@dataclass(frozen=True, slots=True)
class Accounting:
    issuer: Contact
    recipient: Contact
    number_of_people: int
    floor_space: Decimal
    apartment_name: str
    accounting_period: TimePeriod
    usage_period: TimePeriod
    prepaid: Decimal
    allocation_items: Collection[AllocationItem]
    labor_cost_items: Collection[LaborCostItem]
    date: dt.date = field(default_factory=dt.date.today)

    @property
    def refund(self) -> Decimal:
        return self.prepaid - self.gross_total

    @property
    def gross_total(self) -> Decimal:
        return Decimal(sum(i.gross_share for i in self.allocation_items))

    @property
    def labor_costs_total(self) -> Decimal:
        return Decimal(sum(lc.share_amount for lc in self.labor_cost_items))

    @property
    def has_refund(self) -> bool:
        return self.refund >= 0
