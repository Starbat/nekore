import datetime as dt
from dataclasses import dataclass, field
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class Invoice:
    issuer_name: str
    date: dt.date
    gross_amount: Decimal
    privileged_amount: Decimal = field(default_factory=lambda: Decimal("0.00"))
    net_amount: Decimal | None = None
    name: str | None = None

    def __post_init__(self) -> None:
        self._validate_gross_not_less_net()

    def _validate_gross_not_less_net(self) -> None:
        if not self.net_amount:
            return
        if (self.gross_amount < 0) != (self.net_amount < 0):
            raise ValueError("Net amount and gross amount must have the same sign.")
        if (abs(self.gross_amount) - abs(self.net_amount)) < 0:
            raise ValueError("Net amount cannot be greater than gross amount.")
