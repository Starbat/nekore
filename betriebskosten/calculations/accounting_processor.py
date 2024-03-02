from dataclasses import dataclass
from decimal import Decimal
from typing import Final

from betriebskosten.models import (
    Accounting,
    AllocationItem,
    Building,
    Contact,
    InvoiceCollection,
    LaborCostItem,
    Tenant,
    TimePeriod,
)


@dataclass(frozen=True, slots=True)
class AccountingProcessor:
    issuer: Contact
    period: TimePeriod
    building: Building
    invoice_collections: list[InvoiceCollection]

    def create_accountings(self) -> list[Accounting]:
        accountings: Final[list[Accounting]] = []
        for tenant in self.building.get_tenants(self.period):
            accountings.append(self._create_accounting(tenant))
        return accountings

    def _create_accounting(self, tenant: Tenant) -> Accounting:
        labor_cost_items: list[LaborCostItem] = []
        for collection in self.invoice_collections:
            labor_cost_items += [
                item
                for item in self._create_labor_cost_items(collection, tenant)
                if item.share_amount > 0
            ]
        apartment: Final = self.building.get_apartment(tenant)
        return Accounting(
            issuer=self.issuer,
            recipient=tenant.contact,
            number_of_people=tenant.number_of_people,
            floor_space=apartment.floor_space,
            apartment_name=apartment.name or "",
            accounting_period=self.period,
            usage_period=tenant.period,
            prepaid=tenant.prepaid,
            allocation_items=self._create_allocation_items(tenant),
            labor_cost_items=labor_cost_items,
        )

    def _create_allocation_items(self, tenant: Tenant) -> list[AllocationItem]:
        """
        Create allocation items for a tenant's accounting.
        Allocation items with a gross of zero are omitted.
        """
        allocation_items: Final = [
            self._create_allocation_item(collection, tenant)
            for collection in self.invoice_collections
        ]
        return list(filter(lambda i: i.gross_share > 0, allocation_items))

    def _create_allocation_item(
        self, invoice_collection: InvoiceCollection, tenant: Tenant
    ) -> AllocationItem:
        total_shares: Final = invoice_collection.total_shares(
            self.period, self.building
        )
        tenant_shares: Final = invoice_collection.tenant_shares(
            self.period, self.building, tenant
        )
        ratio: Final = tenant_shares / total_shares
        return AllocationItem(
            gross_total=invoice_collection.gross_total,
            gross_share=ratio * invoice_collection.gross_total,
            net_total=invoice_collection.net_total,
            net_share=ratio * invoice_collection.net_total,
            shares_total=total_shares,
            shares_allocated=tenant_shares,
            allocation_name=invoice_collection.allocation_strategy.get_name(),
            name=invoice_collection.name,
        )

    def _create_labor_cost_items(
        self, invoice_collection: InvoiceCollection, tenant: Tenant
    ) -> list[LaborCostItem]:
        total_shares: Final = invoice_collection.total_shares(
            self.period, self.building
        )
        tenant_shares: Final = invoice_collection.tenant_shares(
            self.period, self.building, tenant
        )
        ratio: Final = tenant_shares / total_shares

        issuer_invoices: Final = invoice_collection.get_privileged_invoices_by_issuer()
        return [
            LaborCostItem(
                collection_name=invoice_collection.name,
                issuer_name=issuer,
                gross_amount=Decimal(sum(i.gross_amount for i in invoices)),
                privileged_amount=Decimal(sum(i.privileged_amount for i in invoices)),
                factor=ratio,
                share_amount=ratio * sum(i.privileged_amount for i in invoices),
            )
            for issuer, invoices in issuer_invoices.items()
        ]
