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

        self._amount = amount
        self._date = tx_date
        self._entered = entered
        self._recorded = recorded

    def amount(self):
        """Transaction amount"""
        return self._amount

    def date(self):
        """Transaction date"""
        return self._date

    def entered(self):
        """Date the Transaction was entered in the system"""
        return self._entered

    def is_recorded(self):
        """Is transaction already recorded by bank"""
        return True if self._recorded else False

    def recorded(self):
        """Date the Transaction was recorded by bank"""
        return self._recorded


class Bill(Transaction):
    """
    Represents a bill that's paid from an account.
    """

    def balance_change(self):
        """The actual change to the account balance. Usually equal to amount() or -amount()."""
        return -self._amount


class Deposit(Transaction):
    """
    Represents a deposit to an account.
    """

    def balance_change(self):
        """The actual change to the account balance. Usually equal to amount() or -amount()."""
        return self._amount


class TransferSide:
    """
    Either incoming or outgoing side of a transfer
    """

    def __init__(self, transfer, recorded=None):
        self.transfer = transfer
        self._recorded = recorded

    def amount(self):
        """Transaction amount"""
        return self.transfer.amount()

    def date(self):
        """Transaction date"""
        return self.transfer.date()

    def entered(self):
        """Date the Transaction was entered in the system"""
        return self.transfer.entered()

    def is_recorded(self):
        """Is transfer already recorded by bank on this side?"""
        return True if self._recorded else False

    def recorded(self):
        """Date the Transfer was recorded by bank on this side"""
        return self._recorded


class TransferIn(TransferSide):
    """
    Represents an incoming side of a Transfer
    """

    def balance_change(self):
        """The actual change to the account balance. Usually equal to amount() or -amount()."""
        return self.transfer._amount


class TransferOut(TransferSide):
    """
    Represents an incoming side of a Transfer
    """

    def balance_change(self):
        """The actual change to the account balance. Usually equal to amount() or -amount()."""
        return -self.transfer._amount


class Transfer(Transaction):
    """
    Represents a transfer between accounts
    """

    def __init__(self, amount, tx_date, entered=None, in_recorded=None, out_recorded=None):
        super().__init__(amount, tx_date, entered, recorded=None)

        self._in = TransferIn(self, in_recorded)
        self._out = TransferOut(self, out_recorded)

    def incoming(self):
        """Incoming side of the Transfer"""
        return self._in

    def outgoing(self):
        """Outgoing side of the Transfer"""
        return self._out

    def is_recorded(self):
        """Is this transfer recorded by banks on both sides?"""
        return self._in.is_recorded() and self._out.is_recorded()

    def recorded(self):
        """Date this Transfer was recorded by both banks"""
        if self._in.recorded() and self._out.recorded():
            return max(self._in.recorded(), self._out.recorded())

        return None