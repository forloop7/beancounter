from beancounter.basics.frequency import Daily
from datetime import date


def test_daily_constructor():
    """
    Daily can be constructed
    """
    daily = Daily(date(2011, 12, 31), 2)
    assert daily.step == 2


def test_daily_constructor_defaults():
    """
    Defaults are applied by Daily's constructor
    """
    daily = Daily(date(2016, 2, 2))
    assert daily.step == 1


def test_daily_strings():
    """
    str() and repr() for Daily are correct
    """
    daily = Daily(date(2015, 2, 2), 51)
    assert str(daily) == "Daily(step 51 from 2015-02-02)"
    assert repr(daily) == "Daily(start=datetime.date(2015, 2, 2), step=51)"


def test_daily():
    """
    Basic behavior of Daily Frequency
    """
    daily = Daily(date(2015, 1, 1), 3)
    daily_itr = iter(daily)

    assert next(daily_itr) == date(2015, 1, 1)
    assert next(daily_itr) == date(2015, 1, 4)
