from datetime import date

# TODO: Transfer
# TODO: Seq
# TODO: Status: Entered, Confirmed

class Transaction:
    """
    Base class for all recorded transactions
    """

    def __init__(self, amount, tx_date, entered=None, recorded=None):
        """
        Constructor
        :param amount: transaction amount (Decimal)
        :param tx_date: transaction date 
        :param entered: date it was entered to the system, today() if None
        :param recorded: date it appeared on record (confirmed)
        """
        if not entered:
            entered = date.today()

        self.amount = amount
        self.date = tx_date
        self.entered = entered
        self.recorded = recorded


class Bill(Transaction):
    """
    Represents a bill that's paid from an account.
    """

    def balance_change(self):
        return -self.amount


class Deposit(Transaction):
    """
    Represents a deposit to an account.
    """

    def balance_change(self):
        return self.amount