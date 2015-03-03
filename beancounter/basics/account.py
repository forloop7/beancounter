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

    def __str__(self):
        return "Account('{name}')".format(name=self._name)

    def __repr__(self):
        return "Account('{name}', balance={balance})".format(
            name=self._name, balance=repr(self._balance)
        )

    def enter(self, operation):
        """
        Registers an operation, updating the account balance
        :param transaction:
        """
        self._balance += operation.balance_change()

    def record(self, operation):
        """
        Registers an operation, updating the account balance
        :param transaction:
        """
        self._recorded_balance += operation.balance_change()

    def recorded_balance(self):
        """
        Recorded balance - a balance of an account that includes only recorded transactions
        :return: recorded account balance
        """
        return self._recorded_balance


class Finances:
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
