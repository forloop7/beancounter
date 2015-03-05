from datetime import date


class Transaction:
    """
    Base class for all recorded transactions.

    A transaction consists of one or more operations.
    """

    def __init__(self, tx_date, entered=None):
        """
        Constructor
        :param tx_date: transaction date
        :param entered: date it was entered to the system, today() if None
        """
        self._date = tx_date
        self._entered = entered if entered else date.today()
        self._operations = []

    # TODO: str() and repr()

    def date(self):
        """Transaction date."""
        return self._date

    def entered(self):
        """Date the Transaction was entered in the system."""
        return self._entered

    def operations(self):
        """A list of operations included in this transaction."""
        return self._operations


class Operation:
    """
    Represents an atomic operation performed on a given account.
    """

    def __init__(self, account):
        self._account = account
        self._recorded = None

    def account(self):
        """Account affected by this operation."""
        return self._account

    def recorded(self):
        """Date the Transaction was recorded by bank"""
        return self._recorded


class DepositOperation(Operation):
    """
    Represents a deposit operation
    """

    def __init__(self, transaction, account, recorded=None):
        super().__init__(account)
        self._transaction = transaction

    def balance_change(self):
        return self._transaction._amount


class BillOperation(Operation):
    """
    Represents a bill operation
    """

    def __init__(self, transaction, account, recorded=None):
        super().__init__(account)
        self._transaction = transaction

    def balance_change(self):
        return -self._transaction._amount


class Deposit(Transaction):
    """
    Base class for simple transactions (deposits and bills).

    Simple transactions affect a single account with a single operation.
    """

    def __init__(self, account, amount, tx_date, entered=None):
        """
        Constructor
        :param account: affected account
        :param amount: transaction amount
        :param tx_date: transaction date
        :param entered: date it was entered to the system, today() if None
        """
        super().__init__(tx_date, entered)

        self._amount = amount
        self._operations.append(DepositOperation(self, account))

        # TODO: str() and repr()


class Bill(Transaction):
    """
    Base class for simple transactions (deposits and bills).

    Simple transactions affect a single account with a single operation.
    """

    def __init__(self, account, amount, tx_date, entered=None):
        """
        Constructor
        :param account: affected account
        :param amount: transaction amount
        :param tx_date: transaction date
        :param entered: date it was entered to the system, today() if None
        """
        super().__init__(tx_date, entered)

        self._amount = amount
        self._operations.append(BillOperation(self, account))

        # TODO: str() and repr()


class TransferSide:
    """
    Either incoming or outgoing side of a transfer
    """

    def __init__(self, transfer, recorded=None):
        self._transfer = transfer
        self._recorded = recorded

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
