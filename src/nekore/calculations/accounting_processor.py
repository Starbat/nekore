from dataclasses import dataclass
from itertools import chain
from typing import Collection, Final

from nekore.models import (
    Accounting,
    AllocationItem,
    Building,
    Contact,
    LaborCostItem,
    Tenant,
    TimePeriod,
)

from .invoice_collection_processor import InvoiceCollectionProcessor


@dataclass(frozen=True, slots=True)
class AccountingProcessor:
    issuer: Contact
    period: TimePeriod
    building: Building
    invoice_collection_processors: Collection[InvoiceCollectionProcessor]

    def create_accountings(self) -> list[Accounting]:
        tenants_in_period: Final = self.building.tenants_in(self.period)
        return [self.create_accounting(tenant) for tenant in tenants_in_period]

    def create_accounting(self, tenant: Tenant) -> Accounting:
        apartment: Final = self.building.apartment_of(tenant)
        return Accounting(
            issuer=self.issuer,
            recipient=tenant.contact,
            number_of_people=tenant.number_of_people,
            floor_space=apartment.floor_space,
            apartment_name=apartment.name or "",
            accounting_period=self.period,
            usage_period=tenant.period,
            prepaid=tenant.prepaid,
            allocation_items=self.create_allocation_items(tenant),
            labor_cost_items=self.create_labor_cost_items(tenant),
        )

    def create_allocation_items(self, tenant: Tenant) -> list[AllocationItem]:
        """
        Create allocation items for a tenant's accounting.
        Allocation items with a gross of zero are omitted.
        """
        allocation_items: Final = (
            processor.create_allocation_item(self.building, tenant, self.period)
            for processor in self.invoice_collection_processors
        )
        return list(filter(lambda i: i.gross_share > 0, allocation_items))

    def create_labor_cost_items(self, tenant: Tenant) -> list[LaborCostItem]:
        invoice_processors: Final = (
            p.create_labor_cost_items for p in self.invoice_collection_processors
        )
        item_groups: Final = (
            p(self.building, tenant, self.period) for p in invoice_processors
        )
        items: Final = chain(*item_groups)
        return list(filter(lambda i: i.share_amount > 0, items))
