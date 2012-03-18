from datetime import date, timedelta

def find_week_from_date(t):
    """Return week number (1-52) for the specified date"""
    return t.isocalendar()[:2]

def find_week_from_date_with_offset(t, offset):
    """Returns week number (0-52) for week before date"""
    delta_offset = timedelta(offset)
    return find_week_from_date(t+delta_offset)

def find_start_date_from_week(y, w):
    """Returns a date object for the Monday of a specified week"""
    year = int(y)
    week = int(w)
    t = date(year, 1, 1)
    delta = timedelta(week * 7)
    target = t + delta

    diff = timedelta(target.weekday())
    monday = target - diff

    return monday
