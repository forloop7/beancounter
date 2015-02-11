from datetime import timedelta
from itertools import count


class Frequency:
    """
    Base class for all frequencies
    """

    def since(self, start):
        """
        Abstract method. Returns a generator returning list of dates, starting on start.
        """
        pass


class Daily(Frequency):
    """
    Frequency instance, happening every n days
    """

    def __init__(self, step=1):
        self.step = step

    def __str__(self):
        return "Daily(step {step})".format(step=self.step)

    def __repr__(self):
        return "Daily(step={step})".format(step=self.step)

    def since(self, start):
        """
        Returns a generator containing n-th date, starting from date
        """

        # Wanted to do this, but count() only accepts numbers:
        # return count(start, timedelta(days=self.step))

        next = start
        while (True):
            yield next
            next = next + timedelta(days=self.step)