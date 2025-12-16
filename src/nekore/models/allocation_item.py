from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class AllocationItem:
    name: str
    gross_total: Decimal
    gross_share: Decimal
    shares_total: Decimal
    shares_allocated: Decimal
    allocation_name: str
