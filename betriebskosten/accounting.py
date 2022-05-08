import datetime as dt
from dataclasses import dataclass, field
from decimal import Decimal

from betriebskosten.address import Address
from betriebskosten.allocation_item import AllocationItem
from betriebskosten.labor_cost_item import LaborCostItem
from betriebskosten.time_period import TimePeriod


@dataclass(frozen=True, slots=True)
class Accounting:
    recipient: Address
    number_of_people: int
    accounting_period: TimePeriod
    usage_period: TimePeriod
    prepaid: Decimal
    allocation_items: list[AllocationItem]
    labor_cost_items: list[LaborCostItem]
    labor_costs_total: Decimal = field(init=False)
    gross_total: Decimal = field(init=False)
    refund: Decimal = field(init=False)
    date: dt.date = field(default_factory=dt.date.today)

    def __post_init__(self) -> None:
        object.__setattr__(self, "gross_total", self._allocation_items_gross_total())
        object.__setattr__(self, "refund", self.prepaid - self.gross_total)
        object.__setattr__(self, "labor_costs_total", self._labor_costs_total())

    def _allocation_items_gross_total(self) -> Decimal:
        return Decimal(sum(i.gross_share for i in self.allocation_items))

    def _labor_costs_total(self) -> Decimal:
        return Decimal(sum(lc.share_amount for lc in self.labor_cost_items))
