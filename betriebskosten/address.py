from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Address:
    name: str
    street: str
    house_number: str
    zip_code: str
    city: str
