import pytest
from woodflow import calendar
from datetime import datetime


def test_feb_2026_non_leap():
    # Feb 2026 is not a leap year -> 28 days
    start = 0
    dates, end = calendar.generate_working_dates(2026, 2, start)
    assert all(d.month == 2 and d.year == 2026 for d in dates)
    assert len(dates) == 28
    assert end == (start + 28) % 4


def test_jan_2026_pattern():
    # Jan 4-5 should be working (shift 0,1), Jan 6-7 off (shift 2,3)
    # So start_shift=1 means: Jan 1 shift=1 (work), Jan 2-3 off, Jan 4-5 work, Jan 6-7 off
    start = 1
    dates, end = calendar.generate_working_dates(2026, 1, start)
    days = {d.day for d in dates}
    # Verify 2/2 pattern starting from Jan 4
    assert 4 in days and 5 in days
    assert 6 not in days and 7 not in days
    assert 8 in days and 9 in days
    # Continuity: end shift after January should be (1 + 31) % 4
    assert end == (start + 31) % 4


def test_jan_feb_2026_crossing_working_days():
    # Test continuity: Jan 31 and Feb 1 should follow the cycle
    start = 1  # Jan 1 has shift=1, so Jan 31 has shift=(1+30)%4=3
    jan_dates, end_jan = calendar.generate_working_dates(2026, 1, start)
    # Jan 31 should have shift=3 (off)
    assert jan_dates and jan_dates[-1].day == 31 and jan_dates[-1].month == 1
    # Feb should continue with end_jan shift
    feb_dates, end_feb = calendar.generate_working_dates(2026, 2, end_jan)
    # Feb 1 should have shift = end_jan % 4
    assert feb_dates and feb_dates[0].month == 2 and feb_dates[0].day == 1
    # Verify shifts
    assert end_jan == (start + 31) % 4
