from typing import Final

from betriebskosten.models.allocation_strategy import AllocationStrategy
from betriebskosten.models.invoice import Invoice
from betriebskosten.models.invoice_collection import InvoiceCollection


def test_privileged_invoices(
    dummy_allocation_strategy: AllocationStrategy,
    privileged_invoice: Invoice,
    unprivileged_invoice: Invoice,
) -> None:
    collection: Final = InvoiceCollection(
        "test_collection",
        [privileged_invoice, unprivileged_invoice],
        dummy_allocation_strategy,
    )

    result: Final = collection.privileged_invoices

    assert tuple(result) == (privileged_invoice,)
