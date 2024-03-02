from dataclasses import dataclass

from .bank_account import BankAccount


@dataclass(frozen=True, slots=True)
class Contact:
    name: str
    street: str
    house_number: str
    zip_code: str
    city: str
    bank_account: BankAccount | None = None
