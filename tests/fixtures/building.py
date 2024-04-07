import pytest

from nekore.models import Apartment, Building


@pytest.fixture
def building_a(
    apartment_1_of_building_a: Apartment, apartment_2_of_building_a: Apartment
) -> Building:
    return Building(
        name="Building A",
        apartments=(apartment_1_of_building_a, apartment_2_of_building_a),
    )
