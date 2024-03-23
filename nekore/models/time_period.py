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

    def union(self, *others: Self) -> Self:
        """Create the smallest time period that includes all given time periods."""
        all_periods: Final = others + (self,)
        total_start: Final = min(t.start for t in all_periods)
        total_end: Final = max(t.end for t in all_periods)
        return self.__class__(start=total_start, end=total_end)

    def intersection(self, *others: Self) -> Self | None:
        """
        Calculate the time period included in all periods.
        The duration includes start and end dates.
        """
        all_periods: Final = others + (self,)
        max_start: Final = max(t.start for t in all_periods)
        min_end: Final = min(t.end for t in all_periods)
        if max_start > min_end:
            return None
        return self.__class__(start=max_start, end=min_end)

    def overlaps(self, other: Self) -> bool:
        return bool(self.intersection(other))
