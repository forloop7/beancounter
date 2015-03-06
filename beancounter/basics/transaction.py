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

    def __init__(self, transaction, account):
        self._transaction = transaction
        self._account = account
        self._recorded = None

    def account(self):
        """Account affected by this operation."""
        return self._account

    def recorded(self):
        """Date the Transaction was recorded by bank"""
        return self._recorded

    def record(self, recorded):
        """Records the operation and updates the affected account."""
        if self._recorded:
            raise ValueError('This operation has already been recorded.')
        self._recorded = recorded
        self._account.record(self)


class DepositOperation(Operation):
    """
    Represents a deposit operation
    """

    def balance_change(self):
        return self._transaction._amount


class BillOperation(Operation):
    """
    Represents a bill operation
    """

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


class TransferIn(Operation):
    """
    Represents an incoming side of a Transfer
    """

    def balance_change(self):
        """The actual change to the account_balance. Usually equal to amount() or -amount()."""
        return self._transaction._amount


class TransferOut(Operation):
    """
    Represents an incoming side of a Transfer
    """

    def balance_change(self):
        """The actual change to the account _balance. Usually equal to amount() or -amount()."""
        return -self._transaction._amount


class Transfer(Transaction):
    """
    Represents a transfer between accounts
    """

    def __init__(self, account_from, account_to, amount, tx_date, entered=None):
        """
        Constructor
        :param amount: transfer amount
        :param tx_date: transfer date (when initiated)
        :param entered: date the transfer was entered to the system
        :param out_recorded: date the transfer was recorded at source bank
        :param in_recorded: date the transfer was recorded at destination bank
        :return:
        """
        super().__init__(tx_date, entered)

        self._amount = amount
        self._out = TransferOut(self, account_from)
        self._in = TransferIn(self, account_to)
        self._operations.append(self._out)
        self._operations.append(self._in)

    def amount(self):
        """The transfer amount."""
        return self._amount

    def incoming(self):
        """Incoming side of the Transfer"""
        return self._in

    def outgoing(self):
        """Outgoing side of the Transfer"""
        return self._out

    def recorded(self):
        """Date this Transfer was recorded by both banks"""
        if self._in.recorded() and self._out.recorded():
            return max(self._in.recorded(), self._out.recorded())

        return None
