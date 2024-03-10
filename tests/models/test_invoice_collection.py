from typing import Final

from nekore.models import AllocationStrategy, Invoice, InvoiceCollection


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


def test_privileged_invoices_by_issuer(
    dummy_allocation_strategy: AllocationStrategy,
    privileged_invoice: Invoice,
    unprivileged_invoice: Invoice,
) -> None:
    collection: Final = InvoiceCollection(
        "test_collection",
        [privileged_invoice, unprivileged_invoice],
        dummy_allocation_strategy,
    )

    result: Final = collection.privileged_invoices_by_issuer

    assert result == {privileged_invoice.issuer_name: [privileged_invoice]}


def test_gross_total(
    dummy_allocation_strategy: AllocationStrategy,
    privileged_invoice: Invoice,
    unprivileged_invoice: Invoice,
) -> None:
    collection: Final = InvoiceCollection(
        "test_collection",
        [privileged_invoice, unprivileged_invoice],
        dummy_allocation_strategy,
    )
    assert (
        collection.gross_total
        == privileged_invoice.gross_amount + unprivileged_invoice.gross_amount
    )


def test_net_total(
    dummy_allocation_strategy: AllocationStrategy,
    privileged_invoice: Invoice,
    unprivileged_invoice: Invoice,
) -> None:
    collection: Final = InvoiceCollection(
        "test_collection",
        [privileged_invoice, unprivileged_invoice],
        dummy_allocation_strategy,
    )
    assert (
        collection.net_total
        == privileged_invoice.net_amount + unprivileged_invoice.net_amount
    )
