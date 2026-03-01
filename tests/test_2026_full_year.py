"""Full year 2026 test - verify 2/2 shift pattern for entire year."""
import pytest
from woodflow import calendar


# Expected shift_counter for start of each month (2026 not leap year)
MONTH_STARTS = {
    1: 1,   # Jan
    2: 0,   # Feb
    3: 0,   # Mar
    4: 3,   # Apr
    5: 1,   # May
    6: 0,   # Jun
    7: 2,   # Jul
    8: 1,   # Aug
    9: 0,   # Sep
    10: 2,  # Oct
    11: 1,  # Nov
    12: 3,  # Dec
}

MONTH_NAMES = {
    1: 'January', 2: 'February', 3: 'March', 4: 'April',
    5: 'May', 6: 'June', 7: 'July', 8: 'August',
    9: 'September', 10: 'October', 11: 'November', 12: 'December',
}

DAYS_IN_MONTH = {
    1: 31, 2: 28, 3: 31, 4: 30,
    5: 31, 6: 30, 7: 31, 8: 31,
    9: 30, 10: 31, 11: 30, 12: 31,
}


@pytest.mark.parametrize("month", range(1, 13))
def test_2026_month_2_2_pattern(month):
    """Test that each month follows 2/2 pattern (2 work, 2 off, repeat)."""
    start_shift = MONTH_STARTS[month]
    dates, end_shift = calendar.generate_working_dates(2026, month, start_shift)
    
    # Verify end shift is correct
    expected_end = (start_shift + DAYS_IN_MONTH[month]) % 4
    assert end_shift == expected_end, f"{MONTH_NAMES[month]} end shift mismatch"
    
    # Verify 2/2 pattern: days should follow pattern of 2 work, 2 off, repeat
    day_set = {d.day for d in dates}
    
    # Manual verification: for each 4-day cycle starting from day 1
    days_in_m = DAYS_IN_MONTH[month]
    for day in range(1, days_in_m + 1):
        shift = (start_shift + (day - 1)) % 4
        is_working = shift < 2
        
        if is_working:
            assert day in day_set, f"{MONTH_NAMES[month]} day {day} should be working (shift={shift})"
        else:
            assert day not in day_set, f"{MONTH_NAMES[month]} day {day} should be OFF (shift={shift})"


def test_april_2026_specific():
    """Verify April 2026: 2,3 work; 4,5 off; 6,7 work."""
    dates, _ = calendar.generate_working_dates(2026, 4, MONTH_STARTS[4])
    days = {d.day for d in dates}
    
    assert 2 in days and 3 in days, "April 2-3 must be working"
    assert 4 not in days and 5 not in days, "April 4-5 must be off"
    assert 6 in days and 7 in days, "April 6-7 must be working"


def test_january_2026_specific():
    """Verify January 2026: 1 work, 2-3 off, 4-5 work, 6-7 off."""
    dates, _ = calendar.generate_working_dates(2026, 1, MONTH_STARTS[1])
    days = {d.day for d in dates}
    
    assert 1 in days, "Jan 1 must be working"
    assert 2 not in days and 3 not in days, "Jan 2-3 must be off"
    assert 4 in days and 5 in days, "Jan 4-5 must be working"
    assert 6 not in days and 7 not in days, "Jan 6-7 must be off"


def test_february_2026():
    """Verify February 2026: 1-2 work; 3-4 off; 5-6 work."""
    dates, _ = calendar.generate_working_dates(2026, 2, MONTH_STARTS[2])
    days = {d.day for d in dates}
    
    assert 1 in days and 2 in days, "Feb 1-2 must be working"
    assert 3 not in days and 4 not in days, "Feb 3-4 must be off"
    assert 5 in days and 6 in days, "Feb 5-6 must be working"


def test_july_2026():
    """Verify July 2026: 1-2 off; 3-4 work; 5-6 off."""
    dates, _ = calendar.generate_working_dates(2026, 7, MONTH_STARTS[7])
    days = {d.day for d in dates}
    
    assert 1 not in days and 2 not in days, "Jul 1-2 must be off"
    assert 3 in days and 4 in days, "Jul 3-4 must be working"
    assert 5 not in days and 6 not in days, "Jul 5-6 must be off"
    assert 7 in days and 8 in days, "Jul 7-8 must be working"


def test_december_2026():
    """Verify December 2026: 1 off; 2-3 work; 4-5 off."""
    dates, _ = calendar.generate_working_dates(2026, 12, MONTH_STARTS[12])
    days = {d.day for d in dates}
    
    assert 1 not in days, "Dec 1 must be off"
    assert 2 in days and 3 in days, "Dec 2-3 must be working"
    assert 4 not in days and 5 not in days, "Dec 4-5 must be off"
    assert 6 in days and 7 in days, "Dec 6-7 must be working"


def test_month_continuity():
    """Test that shift_counter flows correctly month to month."""
    current_shift = MONTH_STARTS[1]
    
    for month in range(1, 12):
        dates, end_shift = calendar.generate_working_dates(2026, month, current_shift)
        
        # Verify end shift matches expected
        expected_end = (current_shift + DAYS_IN_MONTH[month]) % 4
        assert end_shift == expected_end
        
        # Next month should start with end_shift
        next_start = MONTH_STARTS[month + 1]
        assert end_shift == next_start, \
            f"Month {month} end ({end_shift}) != Month {month+1} start ({next_start})"
        
        current_shift = end_shift


def test_full_year_working_days():
    """Verify approximately half the days are working in 2026."""
    total_working = 0
    total_days = 0
    
    for month in range(1, 13):
        dates, _ = calendar.generate_working_dates(2026, month, MONTH_STARTS[month])
        total_working += len(dates)
        total_days += DAYS_IN_MONTH[month]
    
    # With 2/2 pattern, should be roughly 50%
    ratio = total_working / total_days
    assert 0.48 < ratio < 0.52, f"Working days ratio {ratio} not close to 50%"
    print(f"2026 working days: {total_working}/{total_days} = {ratio:.1%}")
