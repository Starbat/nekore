from datetime import date, timedelta

from betriebskosten import TimePeriod


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


def test_is_overlapping_lower_range() -> None:
    tp1 = TimePeriod(
        start=date.fromisoformat("2020-01-01"), end=date.fromisoformat("2020-03-01")
    )
    tp2 = TimePeriod(
        start=date.fromisoformat("2020-02-01"), end=date.fromisoformat("2020-04-01")
    )
    assert tp1.is_overlapping_lower_range(tp2)


def test_is_overlapping_upper_range() -> None:
    tp1 = TimePeriod(
        start=date.fromisoformat("2020-02-01"), end=date.fromisoformat("2020-04-01")
    )
    tp2 = TimePeriod(
        start=date.fromisoformat("2020-01-01"), end=date.fromisoformat("2020-03-01")
    )
    assert tp1.is_overlapping_upper_range(tp2)


def test_intersection_handles_non_overlapping() -> None:
    tp1 = TimePeriod(
        start=date.fromisoformat("2020-03-01"), end=date.fromisoformat("2020-04-01")
    )
    tp2 = TimePeriod(
        start=date.fromisoformat("2020-06-01"), end=date.fromisoformat("2020-07-01")
    )

    assert tp1.intersection(tp2) == timedelta(0)
    assert tp2.intersection(tp1) == timedelta(0)


def test_intersection_handles_identical_periods() -> None:
    start = date.fromisoformat("2020-03-01")
    end = date.fromisoformat("2020-04-01")
    delta = end - start + timedelta(days=1)
    tp1, tp2 = (TimePeriod(start=start, end=end) for _ in range(2))

    assert tp1.intersection(tp2) == delta
    assert tp2.intersection(tp1) == delta


def test_intersection_handles_partially_overlapping() -> None:
    tp1 = TimePeriod(
        start=date.fromisoformat("2020-03-10"), end=date.fromisoformat("2020-03-15")
    )
    tp2 = TimePeriod(
        start=date.fromisoformat("2020-03-05"), end=date.fromisoformat("2020-03-13")
    )

    intersection = timedelta(days=4)
    assert tp1.intersection(tp2) == intersection
    assert tp2.intersection(tp1) == intersection


def test_intersection_handles_fully_enclosing() -> None:
    tp1 = TimePeriod(
        start=date.fromisoformat("2020-01-01"), end=date.fromisoformat("2020-01-30")
    )
    tp2 = TimePeriod(
        start=date.fromisoformat("2020-01-10"), end=date.fromisoformat("2020-01-15")
    )

    intersection = timedelta(days=6)
    assert tp1.intersection(tp2) == intersection
    assert tp2.intersection(tp1) == intersection


def test_duration() -> None:
    tp1 = TimePeriod(
        start=date.fromisoformat("2020-01-01"), end=date.fromisoformat("2020-01-03")
    )
    assert tp1.duration == timedelta(days=3)


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


def test_intersection_is_zero_if_other_start_is_after_self_end() -> None:
    tp1 = TimePeriod(
        start=date.fromisoformat("2020-01-01"), end=date.fromisoformat("2020-02-01")
    )
    tp2 = TimePeriod(
        start=date.fromisoformat("2020-03-01"), end=date.fromisoformat("2020-04-01")
    )
    assert tp1.intersection(tp2) == timedelta(days=0)


def test_intersection_is_zero_if_other_end_is_before_self_start() -> None:
    tp1 = TimePeriod(
        start=date.fromisoformat("2020-03-01"), end=date.fromisoformat("2020-04-01")
    )
    tp2 = TimePeriod(
        start=date.fromisoformat("2020-01-01"), end=date.fromisoformat("2020-02-01")
    )
    assert tp1.intersection(tp2) == timedelta(days=0)


def test_intersection_where_self_overlapps_lower_range_of_other() -> None:
    tp1 = TimePeriod(
        start=date.fromisoformat("2020-01-01"), end=date.fromisoformat("2020-01-10")
    )
    tp2 = TimePeriod(
        start=date.fromisoformat("2020-01-05"), end=date.fromisoformat("2020-01-15")
    )
    assert tp1.intersection(tp2) == timedelta(days=6)


def test_intersection_where_self_overlapps_upper_range_of_other() -> None:
    tp1 = TimePeriod(
        start=date.fromisoformat("2020-01-05"), end=date.fromisoformat("2020-01-15")
    )
    tp2 = TimePeriod(
        start=date.fromisoformat("2020-01-01"), end=date.fromisoformat("2020-01-10")
    )
    assert tp1.intersection(tp2) == timedelta(days=6)


def test_intersection_where_time_periods_are_identical() -> None:
    tp1 = TimePeriod(
        start=date.fromisoformat("2020-01-01"), end=date.fromisoformat("2020-01-03")
    )
    tp2 = TimePeriod(
        start=date.fromisoformat("2020-01-01"), end=date.fromisoformat("2020-01-03")
    )
    assert tp1.intersection(tp2) == timedelta(days=3)


def test_intersection_where_self_encloses_other() -> None:
    tp1 = TimePeriod(
        start=date.fromisoformat("2020-01-01"), end=date.fromisoformat("2020-01-10")
    )
    tp2 = TimePeriod(
        start=date.fromisoformat("2020-01-05"), end=date.fromisoformat("2020-01-07")
    )
    assert tp1.intersection(tp2) == timedelta(days=3)


def test_intersection_where_other_encloses_self() -> None:
    tp1 = TimePeriod(
        start=date.fromisoformat("2020-01-05"), end=date.fromisoformat("2020-01-07")
    )
    tp2 = TimePeriod(
        start=date.fromisoformat("2020-01-01"), end=date.fromisoformat("2020-01-10")
    )
    assert tp1.intersection(tp2) == timedelta(days=3)