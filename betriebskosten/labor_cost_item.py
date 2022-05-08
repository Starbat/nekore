from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class LaborCostItem:
    collection_name: str
    issuer_name: str
    gross_amount: Decimal
    privileged_amount: Decimal
    factor: Decimal
    share_amount: Decimal
