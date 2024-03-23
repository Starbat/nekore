from datetime import date, timedelta
from typing import Final

import pytest

from nekore import TimePeriod


def test_contains_date_true() -> None:
    tp1 = TimePeriod(
        start=date.fromisoformat("2020-03-01"), end=date.fromisoformat("2020-04-01")
    )
    assert date.fromisoformat("2020-03-15") in tp1


def test_contains_date_false() -> None:
    tp1 = TimePeriod(
        start=date.fromisoformat("2020-03-01"), end=date.fromisoformat("2020-04-01")
    )
    assert date.fromisoformat("2020-05-15") not in tp1


def test_contains_both_dates_of_other_time_period() -> None:
    tp1 = TimePeriod(
        start=date.fromisoformat("2020-03-01"), end=date.fromisoformat("2020-04-01")
    )
    tp2 = TimePeriod(
        start=date.fromisoformat("2020-03-10"), end=date.fromisoformat("2020-03-15")
    )
    assert tp2 in tp1


def test_contains_one_date_of_other_time_period() -> None:
    tp1 = TimePeriod(
        start=date.fromisoformat("2020-03-01"), end=date.fromisoformat("2020-04-01")
    )
    tp2 = TimePeriod(
        start=date.fromisoformat("2020-03-10"), end=date.fromisoformat("2020-05-01")
    )
    assert tp2 not in tp1


def test_contains_no_date_of_other_time_period() -> None:
    tp1 = TimePeriod(
        start=date.fromisoformat("2020-02-01"), end=date.fromisoformat("2020-03-01")
    )
    tp2 = TimePeriod(
        start=date.fromisoformat("2020-01-01"), end=date.fromisoformat("2020-05-01")
    )
    assert tp2 not in tp1


def test_intersection_handles_non_overlapping() -> None:
    tp1 = TimePeriod(
        start=date.fromisoformat("2020-03-01"), end=date.fromisoformat("2020-04-01")
    )
    tp2 = TimePeriod(
        start=date.fromisoformat("2020-06-01"), end=date.fromisoformat("2020-07-01")
    )

    assert tp1.intersection(tp2) is None
    assert tp2.intersection(tp1) is None


def test_intersection_handles_identical_periods() -> None:
    start = date.fromisoformat("2020-03-01")
    end = date.fromisoformat("2020-04-01")
    tp1, tp2 = (TimePeriod(start=start, end=end) for _ in range(2))

    result_1: Final = tp1.intersection(tp2)
    assert result_1
    assert result_1.start == start and result_1.end == end

    result_2: Final = tp2.intersection(tp1)
    assert result_2
    assert result_2.start == start and result_2.end == end


def test_intersection_handles_partially_overlapping() -> None:
    period_1_start: Final = date.fromisoformat("2020-03-10")
    period_1: Final = TimePeriod(
        start=period_1_start, end=date.fromisoformat("2020-03-15")
    )
    period_2_end: Final = date.fromisoformat("2020-03-13")
    period_2: Final = TimePeriod(
        start=date.fromisoformat("2020-03-05"), end=period_2_end
    )

    result_1: Final = period_1.intersection(period_2)
    assert result_1
    assert result_1.start == period_1_start and result_1.end == period_2_end

    result_2: Final = period_2.intersection(period_1)
    assert result_2
    assert result_2.start == period_1_start and result_2.end == period_2_end


def test_intersection_handles_fully_enclosing() -> None:
    period_1: Final = TimePeriod(
        start=date.fromisoformat("2020-01-01"), end=date.fromisoformat("2020-01-30")
    )
    period_2_start: Final = date.fromisoformat("2020-01-10")
    period_2_end: Final = date.fromisoformat("2020-01-15")
    period_2: Final = TimePeriod(start=period_2_start, end=period_2_end)

    result_1: Final = period_1.intersection(period_2)
    assert result_1
    assert result_1.start == period_2_start and result_1.end == period_2_end

    result_2: Final = period_2.intersection(period_1)
    assert result_2
    assert result_2.start == period_2_start and result_2.end == period_2_end


@pytest.mark.parametrize(
    ("start", "end", "duration"),
    (
        (
            date(year=2020, month=1, day=1),
            date(year=2020, month=1, day=1),
            timedelta(days=1),
        ),
        (
            date(year=2020, month=1, day=1),
            date(year=2020, month=1, day=3),
            timedelta(days=3),
        ),
    ),
)
def test_duration(start: date, end: date, duration: timedelta) -> None:
    assert TimePeriod(start=start, end=end).duration == duration


def test_equals() -> None:
    tp1 = TimePeriod(
        start=date.fromisoformat("2020-01-01"), end=date.fromisoformat("2020-01-01")
    )
    tp2 = TimePeriod(
        start=date.fromisoformat("2020-01-01"), end=date.fromisoformat("2020-01-01")
    )
    assert tp1 == tp2


def test_equals_false() -> None:
    tp1 = TimePeriod(
        start=date.fromisoformat("2020-01-01"), end=date.fromisoformat("2020-01-01")
    )
    tp2 = TimePeriod(
        start=date.fromisoformat("2020-01-01"), end=date.fromisoformat("2020-01-02")
    )
    assert tp1 != tp2


def test_intersection_is_none_if_other_start_is_after_self_end() -> None:
    tp1 = TimePeriod(
        start=date.fromisoformat("2020-01-01"), end=date.fromisoformat("2020-02-01")
    )
    tp2 = TimePeriod(
        start=date.fromisoformat("2020-03-01"), end=date.fromisoformat("2020-04-01")
    )
    assert tp1.intersection(tp2) is None


def test_intersection_is_zero_if_other_end_is_before_self_start() -> None:
    tp1 = TimePeriod(
        start=date.fromisoformat("2020-03-01"), end=date.fromisoformat("2020-04-01")
    )
    tp2 = TimePeriod(
        start=date.fromisoformat("2020-01-01"), end=date.fromisoformat("2020-02-01")
    )
    assert tp1.intersection(tp2) is None


def test_intersection_where_self_overlapps_lower_range_of_other() -> None:
    period_1_end: Final = date.fromisoformat("2020-01-10")
    period_1 = TimePeriod(start=date.fromisoformat("2020-01-01"), end=period_1_end)
    period_2_start: Final = date.fromisoformat("2020-01-05")
    period_2 = TimePeriod(start=period_2_start, end=date.fromisoformat("2020-01-15"))

    result: Final = period_1.intersection(period_2)
    assert result
    assert result.start == period_2_start and result.end == period_1_end


def test_intersection_where_self_overlapps_upper_range_of_other() -> None:
    period_1_start: Final = date.fromisoformat("2020-01-05")
    period_1 = TimePeriod(start=period_1_start, end=date.fromisoformat("2020-01-15"))
    period_2_end: Final = date.fromisoformat("2020-01-10")
    period_2 = TimePeriod(start=date.fromisoformat("2020-01-01"), end=period_2_end)

    result: Final = period_1.intersection(period_2)
    assert result
    assert result.start == period_1_start and result.end == period_2_end


def test_intersection_where_self_encloses_other() -> None:
    period_1 = TimePeriod(
        start=date.fromisoformat("2020-01-01"), end=date.fromisoformat("2020-01-10")
    )
    period_2_start: Final = date.fromisoformat("2020-01-05")
    period_2_end: Final = date.fromisoformat("2020-01-07")
    period_2 = TimePeriod(start=period_2_start, end=period_2_end)

    result: Final = period_1.intersection(period_2)
    assert result
    assert result.start == period_2_start and result.end == period_2_end


def test_intersection_where_other_encloses_self() -> None:
    period_1_start: Final = date.fromisoformat("2020-01-05")
    period_1_end: Final = date.fromisoformat("2020-01-07")
    period_1 = TimePeriod(start=period_1_start, end=period_1_end)
    period_2 = TimePeriod(
        start=date.fromisoformat("2020-01-01"), end=date.fromisoformat("2020-01-10")
    )

    result: Final = period_1.intersection(period_2)
    assert result
    assert result.start == period_1_start and result.end == period_1_end


def test_overlaps_true() -> None:
    t1, t2 = (
        TimePeriod(start=date.fromisoformat(start), end=date.fromisoformat(end))
        for start, end in (("2020-01-05", "2020-01-07"), ("2020-01-06", "2020-01-08"))
    )
    assert t1.overlaps(t2)


def test_overlaps_false() -> None:
    t1, t2 = (
        TimePeriod(start=date.fromisoformat(start), end=date.fromisoformat(end))
        for start, end in (("2020-01-05", "2020-01-07"), ("2020-01-09", "2020-01-11"))
    )
    assert not t1.overlaps(t2)


def test_union_with_single_other() -> None:
    date_1: Final = date(year=2020, month=1, day=1)
    later_dates: Final = tuple(date_1 + timedelta(days=f * 100) for f in range(1, 4))
    dates = (date_1,) + later_dates

    period_1: Final = TimePeriod(start=dates[0], end=dates[1])
    period_2: Final = TimePeriod(start=dates[2], end=dates[3])

    result: Final = period_1.union(period_2)

    assert result.start == dates[0]
    assert result.end == dates[-1]


def test_union_with_multiple_others() -> None:
    date_1: Final = date(year=2020, month=1, day=1)
    later_dates: Final = tuple(date_1 + timedelta(days=f * 100) for f in range(1, 6))
    dates = (date_1,) + later_dates

    period_1: Final = TimePeriod(start=dates[0], end=dates[1])
    period_2: Final = TimePeriod(start=dates[2], end=dates[3])
    period_3: Final = TimePeriod(start=dates[4], end=dates[5])

    result: Final = period_1.union(period_2, period_3)

    assert result.start == dates[0]
    assert result.end == dates[5]
