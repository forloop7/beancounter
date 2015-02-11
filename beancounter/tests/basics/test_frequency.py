from beancounter.basics.frequency import Daily
from datetime import date


def test_daily_constructor():
    """
    Daily can be constructed
    """
    daily = Daily(2)
    assert daily.step == 2


def test_daily_constructor_defaults():
    """
    Defaults are applied by Daily's constructor
    """
    daily = Daily()
    assert daily.step == 1


def test_daily_strings():
    """
    str() and repr() for Daily ae correct
    """
    daily = Daily(51)
    assert str(daily) == "Daily(step 51)"
    assert repr(daily) == "Daily(step=51)"


def test_daily():
    """
    Basic behavior of Daily Frequency
    """
    daily = Daily(3)
    daily_itr = daily.since(date(2015, 1, 1))

    assert next(daily_itr) == date(2015, 1, 1)
    assert next(daily_itr) == date(2015, 1, 4)
