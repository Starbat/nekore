from dataclasses import dataclass
from decimal import Decimal
from typing import Final

from nekore.models import (
    AllocationItem,
    Building,
    InvoiceCollection,
    LaborCostItem,
    Tenant,
    TimePeriod,
)
from nekore.models.allocation_strategy import AllocationStrategy


@dataclass(slots=True, frozen=True)
class InvoiceCollectionProcessor:
    invoice_collection: InvoiceCollection
    allocation_strategy: AllocationStrategy

    def total_shares(
        self, accounting_period: TimePeriod, building: Building
    ) -> Decimal:
        return self.allocation_strategy.total_shares(accounting_period, building)

    def tenant_shares(
        self, accounting_period: TimePeriod, building: Building, tenant: Tenant
    ) -> Decimal:
        return self.allocation_strategy.tenant_shares(
            accounting_period, building, tenant
        )

    def create_allocation_item(
        self, building: Building, tenant: Tenant, period: TimePeriod
    ) -> AllocationItem:
        total_shares: Final = self.total_shares(period, building)
        tenant_shares: Final = self.tenant_shares(period, building, tenant)
        ratio: Final = tenant_shares / total_shares
        return AllocationItem(
            gross_total=self.invoice_collection.gross_total,
            gross_share=ratio * self.invoice_collection.gross_total,
            net_total=self.invoice_collection.net_total,
            net_share=ratio * self.invoice_collection.net_total,
            shares_total=total_shares,
            shares_allocated=tenant_shares,
            allocation_name=self.allocation_strategy.name,
            name=self.invoice_collection.name,
        )

    def create_labor_cost_items(
        self, building: Building, tenant: Tenant, period: TimePeriod
    ) -> list[LaborCostItem]:
        total_shares: Final = self.total_shares(period, building)
        tenant_shares: Final = self.tenant_shares(period, building, tenant)
        ratio: Final = tenant_shares / total_shares

        issuer_invoices: Final = self.invoice_collection.privileged_invoices_by_issuer
        return [
            LaborCostItem(
                collection_name=self.invoice_collection.name,
                issuer_name=issuer,
                gross_amount=Decimal(sum(i.gross_amount for i in invoices)),
                privileged_amount=Decimal(sum(i.privileged_amount for i in invoices)),
                factor=ratio,
                share_amount=ratio * sum(i.privileged_amount for i in invoices),
            )
            for issuer, invoices in issuer_invoices.items()
        ]
