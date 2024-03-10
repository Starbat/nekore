import datetime as dt
from dataclasses import dataclass, field
from typing import Self


@dataclass(frozen=True, eq=True, slots=True)
class TimePeriod:
    """A period between two dates."""

    start: dt.date
    end: dt.date
    duration: dt.timedelta = field(init=False)

    def __post_init__(self) -> None:
        if self.start > self.end:
            raise ValueError("Start cannot be greater than end.")
        object.__setattr__(
            self, "duration", self.end - self.start + dt.timedelta(days=1)
        )

    def __contains__(self, other: dt.date | Self) -> bool:
        if isinstance(other, dt.date):
            return self.start <= other <= self.end
        return self.start <= other.start <= other.end <= self.end

    def is_overlapping_lower_range(self, other: Self) -> bool:
        return other.start in self and other.end not in self

    def is_overlapping_upper_range(self, other: Self) -> bool:
        return other.end in self and other.start not in self

    def intersection(self, other: Self) -> dt.timedelta:
        """
        Calculate the amount of time included in both periods.
        The duration includes start and end dates.
        """
        if self == other:
            return self.duration
        if self.is_overlapping_lower_range(other):
            return self.end - other.start + dt.timedelta(days=1)
        if self.is_overlapping_upper_range(other):
            return other.end - self.start + dt.timedelta(days=1)
        if other in self:
            return other.duration
        if self in other:
            return self.duration
        return dt.timedelta(0)
