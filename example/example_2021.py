from datetime import date
from decimal import Decimal

from nekore import (
    AccountingProcessor,
    Apartment,
    ApartmentStrategy,
    BankAccount,
    Building,
    Contact,
    DirectInvoiceStrategy,
    DocumentGenerator,
    FloorAreaStrategy,
    Invoice,
    InvoiceCollection,
    InvoiceCollectionProcessor,
    Tenant,
    TimePeriod,
)

apartment_address = {
    "street": "Some street",
    "house_number": "70",
    "zip_code": "12345",
    "city": "Some city",
}

schwarz, fuchs, anderson = (
    Tenant(
        contact=Contact(name=name, **apartment_address),
        number_of_people=people,
        period=TimePeriod(date.fromisoformat(start), date.fromisoformat(end)),
        prepaid=Decimal(prepaid),
    )
    for name, prepaid, people, start, end in (
        ("Amanda Schwarz", 380.00, 3, "2021-01-01", "2021-06-30"),
        ("Peter Fuchs", 400.00, 1, "2021-07-01", "2021-12-31"),
        ("Family Anderson", 130.00, 4, "2018-04-01", "2022-01-31"),
    )
)

apartment_building = Building(
    name="apartment building in some street 70",
    apartments=[
        Apartment(
            name="ground floor", floor_space=Decimal(120), tenants=[schwarz, fuchs]
        ),
        Apartment(name="first floor", floor_space=Decimal(100), tenants=[anderson]),
    ],
)

land_tax_invoices = InvoiceCollection(
    name="Land tax",
    invoices=[
        Invoice(
            "Municipal authorities",
            gross_amount=Decimal(600),
            net_amount=Decimal(600),
            date=date.fromisoformat("2021-08-14"),
        )
    ],
)

gardening_invoices = InvoiceCollection(
    name="Gardening",
    invoices=[
        Invoice(
            "Some Gardener",
            gross_amount=Decimal(599.46),
            net_amount=Decimal(503.75),
            privileged_amount=Decimal(599.46),
            date=date.fromisoformat("2021-03-08"),
        ),
        Invoice(
            "Another Gardener",
            gross_amount=Decimal(1428),
            net_amount=Decimal(1200),
            privileged_amount=Decimal(500),
            date=date.fromisoformat("2021-08-06"),
        ),
    ],
)

schwarz_direct_invoices = InvoiceCollection(
    name="Heating maintenance",
    invoices=[
        Invoice(
            "Some heating technician",
            date=date.fromisoformat("2021-10-02"),
            gross_amount=Decimal(119),
            net_amount=Decimal(100),
            privileged_amount=Decimal(119),
        )
    ],
)


accounting_processor = AccountingProcessor(
    issuer=Contact(
        name="Me",
        city="My city",
        street="My street",
        house_number="12",
        zip_code="2345",
        bank_account=BankAccount(
            iban="DE22 1001 0050 0123 4567 89", bic="AAAA BB 11 222", bank="My bank"
        ),
    ),
    period=TimePeriod(
        start=date.fromisoformat("2021-01-01"),
        end=date.fromisoformat("2021-12-31"),
    ),
    building=apartment_building,
    invoice_collection_processors=[
        InvoiceCollectionProcessor(land_tax_invoices, FloorAreaStrategy()),
        InvoiceCollectionProcessor(gardening_invoices, ApartmentStrategy()),
        InvoiceCollectionProcessor(
            schwarz_direct_invoices, DirectInvoiceStrategy(tenant=schwarz)
        ),
    ],
)

accountings = accounting_processor.create_accountings()

document_generator = DocumentGenerator()

document_generator.create_documents("./output", accountings)
