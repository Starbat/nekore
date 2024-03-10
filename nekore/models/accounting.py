import datetime as dt
from dataclasses import dataclass, field
from decimal import Decimal

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
    allocation_items: list[AllocationItem]
    labor_cost_items: list[LaborCostItem]
    labor_costs_total: Decimal = field(init=False)
    date: dt.date = field(default_factory=dt.date.today)

    def __post_init__(self) -> None:
        object.__setattr__(self, "labor_costs_total", self._labor_costs_total())

    @property
    def refund(self) -> Decimal:
        return self.prepaid - self.gross_total

    @property
    def gross_total(self) -> Decimal:
        return Decimal(sum(i.gross_share for i in self.allocation_items))

    def _labor_costs_total(self) -> Decimal:
        return Decimal(sum(lc.share_amount for lc in self.labor_cost_items))

    @property
    def has_refund(self) -> bool:
        return self.refund >= 0
