from datetime import date, timedelta

def find_week_from_date(t):
    """Return week number (1-52) for the specified date"""
    return t.isocalendar()[:2]

def find_week_from_date_with_offset(t, offset):
    """Returns week number (0-52) for week before date"""
    delta_offset = timedelta(offset)
    return find_week_from_date(t+delta_offset)

def find_start_date_from_date(t):
    """Returns a date object for the Sunday directly before a specified date"""
    # weekday gives us monday = 0 ... sunday = 6.  Add 1 and modulo 7 to get
    # sunday = 0 .. saturday = 6
    weekday = (t.weekday() + 1) % 7
    delta = timedelta(weekday)

    return t - delta

def string_date_to_date(i):
    """Converts '20120328' to date(2012, 3, 28)"""
    y = int(i[:4])
    m = int(i[4:6])
    d = int(i[6:])
    return date(y, m, d)
