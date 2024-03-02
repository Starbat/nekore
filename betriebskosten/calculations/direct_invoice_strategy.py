from dataclasses import dataclass
from decimal import Decimal
from typing import Any

from betriebskosten.models import Tenant


@dataclass(frozen=True, slots=True)
class DirectInvoiceStrategy:
    tenant: Tenant
    name: str = "Direkt"

    def get_name(self) -> str:
        return self.name

    def total_shares(self, *_: Any) -> Decimal:
        return Decimal("1")

    def tenant_shares(self, _: Any, __: Any, tenant: Tenant) -> Decimal:
        return Decimal("1") if tenant == self.tenant else Decimal(0)
