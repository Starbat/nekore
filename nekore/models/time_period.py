import datetime as dt
from dataclasses import dataclass
from typing import Self


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

    def only_contains_start(self, other: Self) -> bool:
        return other.start in self and other.end not in self

    def only_contains_end(self, other: Self) -> bool:
        return other.end in self and other.start not in self

    def intersection(self, other: Self) -> dt.timedelta:
        """
        Calculate the amount of time included in both periods.
        The duration includes start and end dates.
        """
        if self == other:
            return self.duration
        if self.only_contains_start(other):
            return self.end - other.start + dt.timedelta(days=1)
        if self.only_contains_end(other):
            return other.end - self.start + dt.timedelta(days=1)
        if other in self:
            return other.duration
        if self in other:
            return self.duration
        return dt.timedelta(0)

    def overlaps(self, other: Self) -> bool:
        return bool(self.intersection(other))
