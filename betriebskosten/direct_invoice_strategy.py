from dataclasses import dataclass
from decimal import Decimal
from typing import Any

from .tenant import Tenant


@dataclass(frozen=True, slots=True)
class DirectInvoiceStrategy:
    name: str
    tenant: Tenant

    def total_shares(self, *args: Any) -> Decimal:
        return Decimal("1")

    def tenant_shares(self, _: Any, __: Any, tenant: Tenant) -> Decimal:
        return Decimal("1") if tenant == self.tenant else Decimal(0)
