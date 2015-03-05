from decimal import Decimal
from beancounter.basics.transaction import Deposit, Bill, Transfer


class Account:
    """
    Represents an account (a place to keep cash)
    """

    def __init__(self, name, balance=Decimal('0.00')):
        self._name = name
        self._balance = balance
        self._recorded_balance = balance
        self._initial_balance = self._balance

    def name(self):
        """Returns Account name"""
        return self._name

    def balance(self):
        """Returns the current balance"""
        return self._balance

    def recorded_balance(self):
        """
        Recorded balance - a balance of an account that includes only recorded transactions
        """
        return self._recorded_balance

    def __str__(self):
        return "Account('{name}')".format(name=self._name)

    def __repr__(self):
        return "Account('{name}', balance={balance})".format(
            name=self._name, balance=repr(self._balance)
        )

    def enter(self, operation):
        """
        Registers an operation, updating the account balance
        :param operation:
        """
        self._balance += operation.balance_change()

    def record(self, operation):
        """
        Registers an operation, updating the account balance
        :param operation:
        """
        self._recorded_balance += operation.balance_change()


class Logbook:
    """
    Container class for all finances, accounts, transactions and budget.
    """

    def __init__(self, accounts=[], transactions=[]):
        """
        Constructor.
        :param accounts: list of accounts included in the finances being tracked
        :return: new Finances object.
        """
        self.accounts = accounts
        self.transactions = transactions

    def add_account(self, name, balance=Decimal('0.00')):
        """
        TODO: docstring :-)
        """
        account = Account(self, name, balance=balance)
        self.accounts.append(account)
        return account

    def deposit(self, account, amount, tx_date, entered=None, recorded=None):
        """
        Enters a deposit to an account into the log.
        """
        deposit = Deposit(account, amount, tx_date, entered)
        self.enter(deposit)

    def bill(self, account, amount, tx_date, entered=None, recorded=None):
        """
        Enters a deposit to an account into the log.
        """
        bill = Bill(account, amount, tx_date, entered)
        self.enter(bill)

    def enter(self, transaction):
        """
        Enters a transaction into the log.
        """
        self.transactions.append(transaction)
        for operation in transaction.operations():
            operation.account().enter(operation)

    def record():
        # TODO: implement
        pass
