from decimal import Decimal
from typing import Final

from nekore.calculations.resident_number_strategy import ResidentNumberStrategy
from nekore.models import Building, TimePeriod


class TestResidentNumberStrategy:
    @staticmethod
    def test_total_shares(year_2020: TimePeriod, building_a: Building) -> None:
        strategy: Final = ResidentNumberStrategy()

        result: Final = strategy.total_shares(year_2020, building_a)

        assert result == 3
