from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class BankAccount:
    iban: str
    bic: str
    bank: str
