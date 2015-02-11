from decimal import Decimal


class Account:
    """
    Represents an account (a place to keep cash)
    """

    def __init__(self, name):
        self.name = name
        self.seq = 0
        self.balance = Decimal('0.00')

    def __str__(self):
        return "Account({name})".format(name=self.name)

    def __repr__(self):
        return "Account({name}, seq={seq}, balance={balance})".format(
            name=self.name, seq=self.seq, balance=repr(self.balance)
        )