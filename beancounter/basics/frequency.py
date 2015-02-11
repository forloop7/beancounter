from datetime import timedelta, date
from itertools import count


class Frequency:
    """
    Base class for all frequencies
    """

    def __iter__(self):
        """
        Abstract. When implemented it should return an iterator for list of dates, starting on start.
        """
        pass


class Daily(Frequency):
    """
    Frequency instance, happening every n days
    """

    def __init__(self, start, step=1):
        self.start = start
        self.step = step

    def __str__(self):
        return "Daily(step {step} from {start})".format(step=self.step, start=self.start)

    def __repr__(self):
        return "Daily(start={start}, step={step})".format(start=repr(self.start), step=self.step)

    def __iter__(self):
        """
        Returns a generator containing n-th date
        """

        # Wanted to do this, but count() only accepts numbers:
        # return count(start, timedelta(days=self.step))

        next = self.start
        while (True):
            yield next
            next = next + timedelta(days=self.step)