from decimal import Decimal
from beancounter.basics.transaction import Deposit, Bill, Transfer
from beancounter.basics.utils import are_equal


class Account:
    """
    Represents an account (a place to keep cash)
    """

    def __init__(self, logbook, name, balance=Decimal('0.00')):
        self._name = name
        self._balance = balance
        self._initial_balance = self._balance
        self._logbook = logbook

    def name(self):
        """Returns Account name"""
        return self._name

    def balance(self):
        """Returns the current balance"""
        return self._balance

    def transactions(self):
        """Returns list of transactions entered for this account"""
        return [tx for tx in self._logbook.transactions if tx.account() is self]

    def __str__(self):
        return "Account('{name}')".format(name=self._name)

    def __repr__(self):
        return "Account('{name}', balance={balance})".format(
            name=self._name, balance=repr(self._balance)
        )

    def __eq__(self, other):
        """
        Compares two Accounts, by their types and fields
        :param other: Transaction to be compared to
        :return: True if this and other are of the same type and have the same fields' values
        """
        if type(self) is type(other):
            if self.transactions() != other.transactions():
                return False
            return are_equal(self.__dict__, other.__dict__, exclude=['_logbook'])
        else:
            return False

    def register(self, transaction):
        """
        Registers a transaction, updating the account balance
        :param transaction:
        """
        self._logbook.transactions.append(transaction)
        self._balance += transaction.balance_change()

    def deposit(self, amount, deposit_date):
        """
        Deposit money to the account
        :param amount: amount, right? Make it Decimal
        :return: Deposit object representing the new deposit
        """
        deposit = Deposit(self, amount, deposit_date)
        self.register(deposit)
        return deposit

    def bill(self, amount, bill_date):
        """
        Deposit money to the account
        :param amount: amount, right? Make it Decimal
        :return: Bill object representing the new bill
        """
        bill = Bill(self, amount, bill_date)
        self.register(bill)
        return bill

    def transfer(self, to_account, amount, tx_date, entered=None, recorded=None,
                 dest_recorded=None):
        transfer = Transfer(self, to_account, amount, tx_date, entered, recorded, dest_recorded)
        self.register(transfer.outgoing())
        to_account.register(transfer.incoming())
        return transfer

    def recorded_balance(self):
        """
        Recorded balance - a balance of an account that includes only recorded transactions
        :return: recorded account balance
        """
        recorded_change = sum(t.balance_change() for t in self.transactions() if t.is_recorded())
        return self._initial_balance + recorded_change


class Finances:
    """
    Container class for all finances, accounts, transactions and budget.
    """

    def __init__(self, transactions=[]):
        """
        Constructor.
        :param accounts: list of accounts included in the finances being tracked
        :return: new Finances object.
        """
        self.accounts = []
        self.transactions = transactions

    def __eq__(self, other):
        """
        Compares two Finances, by their types and fields
        :param other: Finances object to be compared to
        :return: True if this and other are of the same type and have the same fields' values
        """
        if type(self) is type(other):
            return self.__dict__ == other.__dict__
        else:
            return False

    def add_account(self, name, balance=Decimal('0.00')):
        """
        TODO: docstring :-)
        """
        account = Account(self, name, balance=balance)
        self.accounts.append(account)
        return account
