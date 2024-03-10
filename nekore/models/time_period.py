import datetime as dt
from dataclasses import dataclass
from typing import Final, Self


@dataclass(frozen=True, eq=True, slots=True)
class TimePeriod:
    """A period between two dates."""

    start: dt.date
    end: dt.date

    def __post_init__(self) -> None:
        if self.start > self.end:
            raise ValueError("Start cannot be greater than end.")

    @property
    def duration(self) -> dt.timedelta:
        return self.end - self.start + dt.timedelta(days=1)

    def __contains__(self, other: dt.date | Self) -> bool:
        if isinstance(other, dt.date):
            return self.start <= other <= self.end
        return self.start <= other.start <= other.end <= self.end

    @classmethod
    def cover(cls, *time_periods: Self) -> Self:
        """Create the smallest time period that includes all given time periods."""
        total_start: Final = min(t.start for t in time_periods)
        total_end: Final = max(t.end for t in time_periods)
        return cls(start=total_start, end=total_end)

    def intersection(self, other: Self) -> dt.timedelta:
        """
        Calculate the amount of time included in both periods.
        The duration includes start and end dates.
        """
        total_period: Final = self.cover(self, other)
        start_difference: Final = abs(self.start - other.start)
        end_difference: Final = abs(self.end - other.end)
        overlap: Final = total_period.duration - start_difference - end_difference
        return max(overlap, dt.timedelta(0))

    def overlaps(self, other: Self) -> bool:
        return bool(self.intersection(other))
