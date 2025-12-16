from dataclasses import dataclass
from decimal import Decimal
from typing import Collection, Final, Iterator

from .invoice import Invoice


@dataclass(frozen=True, slots=True)
class InvoiceCollection:
    name: str
    invoices: Collection[Invoice]

    @property
    def gross_total(self) -> Decimal:
        """The sum of the gross amounts of all included invoices"""
        return Decimal(sum(i.gross_amount for i in self.invoices))

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
