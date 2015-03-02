from datetime import date
from beancounter.basics.utils import are_equal


class Transaction:
    """
    Base class for all recorded transactions
    """

    def __init__(self, account, amount, tx_date, entered=None, recorded=None):
        """
        Constructor
        :param amount: transaction amount (Decimal)
        :param tx_date: transaction date 
        :param entered: date it was entered to the system, today() if None
        :param recorded: date it appeared on record (confirmed)
        """
        if not entered:
            entered = date.today()

        self._account = account
        self._amount = amount
        self._date = tx_date
        self._entered = entered
        self._recorded = recorded

    def __eq__(self, other):
        """
        Compares two Transactions, by their types and fields
        :param other: Transaction to be compared to
        :return: True if this and other are of the same type and have the same fields' values
        """
        if type(self) is type(other):
            return are_equal(self.__dict__, other.__dict__, exclude=['_account'])
        else:
            return False

    # TODO: str() and repr()

    def account(self):
        """Transaction account"""
        return self._account

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

    def record(self, recorded_date):
        """
        Records the transaction with the date specified
        :param recorded_date: date of recording
        """
        self._recorded = recorded_date


class Bill(Transaction):
    """
    Represents a bill that's paid from an account.
    """

    def balance_change(self):
        """The actual change to the account _balance. Usually equal to amount() or -amount()."""
        return -self._amount


class Deposit(Transaction):
    """
    Represents a deposit to an account.
    """

    def balance_change(self):
        """The actual change to the account _balance. Usually equal to amount() or -amount()."""
        return self._amount


class TransferSide:
    """
    Either incoming or outgoing side of a transfer
    """

    def __init__(self, transfer, recorded=None):
        self._transfer = transfer
        self._recorded = recorded

    def __eq__(self, other):
        """
        Compares two TransferSides, by their types and fields
        :param other: TransferSide to be compared to
        :return: True if this and other are of the same type and have the same fields' values
        """
        # Note: Can't compare __dict__'s, as this compares _transaction's which causes an infinite
        # recursion
        if type(self) is type(other):
            return (self._transfer == other._transfer)
        else:
            return False

    def amount(self):
        """Transaction amount"""
        return self._transfer.amount()

    def date(self):
        """Transaction date"""
        return self._transfer.date()

    def entered(self):
        """Date the Transaction was entered in the system"""
        return self._transfer.entered()

    def is_recorded(self):
        """Is transfer already recorded by bank on this side?"""
        return True if self._recorded else False

    def recorded(self):
        """Date the Transfer was recorded by bank on this side"""
        return self._recorded

    def record(self, recorded_date):
        """Records the transfer on this side"""
        self._recorded = recorded_date


class TransferIn(TransferSide):
    """
    Represents an incoming side of a Transfer
    """

    def account(self):
        """The account being affected."""
        return self._transfer._account_to
    
    def balance_change(self):
        """The actual change to the account_balance. Usually equal to amount() or -amount()."""
        return self._transfer._amount


class TransferOut(TransferSide):
    """
    Represents an incoming side of a Transfer
    """

    def account(self):
        """The account being affected."""
        return self._transfer._account
    
    def balance_change(self):
        """The actual change to the account _balance. Usually equal to amount() or -amount()."""
        return -self._transfer._amount


class Transfer(Transaction):
    """
    Represents a transfer between accounts
    """

    def __init__(self, account_from, account_to, amount, tx_date, entered=None, out_recorded=None, in_recorded=None):
        """
        Constructor
        :param amount: transfer amount
        :param tx_date: transfer date (when initiated)
        :param entered: date the transfer was entered to the system
        :param out_recorded: date the transfer was recorded at source bank
        :param in_recorded: date the transfer was recorded at destination bank
        :return:
        """
        super().__init__(account_from, amount, tx_date, entered, recorded=None)

        self._out = TransferOut(self, out_recorded)
        self._in = TransferIn(self, in_recorded)
        self._account_to = account_to

    def __eq__(self, other):
        """
        Compares two Transfers, by their types and fields
        :param other: Transfer to be compared to
        :return: True if this and other are of the same type and have the same fields' values
        """
        if type(self) is type(other):
            return (are_equal(self.__dict__, other.__dict__, exclude=['_account', '_account_to', 
                                                                      '_out', '_in']) and
                    self._out._recorded == other._out._recorded and
                    self._in._recorded == other._in._recorded)
        else:
            return False

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
