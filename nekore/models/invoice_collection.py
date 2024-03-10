from dataclasses import dataclass, field
from decimal import Decimal
from typing import Final, Iterator

from .allocation_strategy import AllocationStrategy
from .building import Building
from .invoice import Invoice
from .tenant import Tenant
from .time_period import TimePeriod


@dataclass(frozen=True, slots=True)
class InvoiceCollection:
    name: str
    invoices: list[Invoice]
    allocation_strategy: AllocationStrategy
    net_total: Decimal = field(init=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "net_total", self._net_total())

    @property
    def gross_total(self) -> Decimal:
        """The sum of the gross amounts of all included invoices"""
        return Decimal(sum(i.gross_amount for i in self.invoices))

    def _net_total(self) -> Decimal:
        """Calculates the net total of a sequence of invoices."""
        return Decimal(sum([i.net_amount for i in self.invoices]))

    def total_shares(
        self,
        accounting_period: TimePeriod,
        building: Building,
    ) -> Decimal:
        return self.allocation_strategy.total_shares(accounting_period, building)

    def tenant_shares(
        self,
        accounting_period: TimePeriod,
        building: Building,
        tenant: Tenant,
    ) -> Decimal:
        return self.allocation_strategy.tenant_shares(
            accounting_period, building, tenant
        )

    @property
    def privileged_invoices(self) -> Iterator[Invoice]:
        return filter(lambda i: i.privileged_amount > 0, self.invoices)

    @property
    def privileged_invoices_by_issuer(self) -> dict[str, list[Invoice]]:
        issuer_invoices: Final[dict[str, list[Invoice]]] = dict()
        for invoice in self.privileged_invoices:
            if invoice.issuer_name in issuer_invoices:
                issuer_invoices[invoice.issuer_name].append(invoice)
            else:
                issuer_invoices[invoice.issuer_name] = [invoice]
        return issuer_invoices
