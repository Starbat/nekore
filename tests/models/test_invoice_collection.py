from typing import Final

from nekore.models import Invoice, InvoiceCollection


def test_privileged_invoices(
    privileged_invoice: Invoice,
    unprivileged_invoice: Invoice,
) -> None:
    collection: Final = InvoiceCollection(
        "test_collection", [privileged_invoice, unprivileged_invoice]
    )

    result: Final = collection.privileged_invoices

    assert tuple(result) == (privileged_invoice,)


def test_privileged_invoices_by_issuer(
    privileged_invoice: Invoice,
    unprivileged_invoice: Invoice,
) -> None:
    collection: Final = InvoiceCollection(
        "test_collection", [privileged_invoice, unprivileged_invoice]
    )

    result: Final = collection.privileged_invoices_by_issuer

    assert result == {privileged_invoice.issuer_name: [privileged_invoice]}


def test_gross_total(
    privileged_invoice: Invoice,
    unprivileged_invoice: Invoice,
) -> None:
    collection: Final = InvoiceCollection(
        "test_collection", [privileged_invoice, unprivileged_invoice]
    )
    assert (
        collection.gross_total
        == privileged_invoice.gross_amount + unprivileged_invoice.gross_amount
    )
