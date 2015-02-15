from beancounter import Account
from decimal import Decimal
from datetime import date


def test_creation():
    """
    Basic properties of Account constructor.
    """
    acc = Account('Some account')

    assert acc.name() == 'Some account'
    assert acc.balance() == Decimal('0.00')


def test_strings():
    """
    str(account) and repr(account)
    """
    acc = Account('Some acc')

    assert str(acc) == "Account(Some acc)"
    assert repr(acc) == "Account(Some acc, balance=Decimal('0.00'))"


def test_bill_balance():
    """
    Bills can be paid from an account, updating balance
    """
    acc = Account('Some account')

    acc.deposit(Decimal('100.00'), date.today())
    assert acc.balance() == Decimal('100.00')


def test_bill_balance2():
    """
    Bills can be paid from an account, updating balance
    """
    acc = Account('Some account')

    acc.deposit(Decimal('100.00'), date.today())
    acc.deposit(Decimal('120.00'), date.today())
    assert acc.balance() == Decimal('220.00')


def test_deposits_list():
    """
    Bills can be paid from an account, updating balance
    """
    acc = Account('Some account')
    amount = Decimal('120.00')
    deposit1_date = date(2014, 1, 5)
    deposit2_date = date(2014, 2, 5)
    acc.deposit(amount, deposit1_date)
    acc.deposit(2 * amount, deposit2_date)
    assert len(acc.transactions()) == 2

    deposit1 = acc.transactions()[0]
    deposit2 = acc.transactions()[1]
    assert deposit1.amount() == amount
    assert deposit1.date() == deposit1_date
    assert deposit1.entered() == date.today()
    assert deposit2.amount() == 2 * amount
    assert deposit2.date() == deposit2_date
    assert deposit2.entered() == date.today()
    assert acc.balance() == 3 * amount


def test_bills_list():
    """
    Bills can be paid from an account, updating balance
    """
    acc = Account('Some account')
    amount = Decimal('120.00')
    bill_date = date(2014, 1, 5)
    acc.deposit(4 * amount, date(2011, 12, 31))
    acc.bill(amount, bill_date)
    assert len(acc.transactions()) == 2

    bill = acc.transactions()[1]
    assert bill.amount() == amount
    assert bill.date() == bill_date
    assert bill.entered() == date.today()
    assert acc.balance() == 3 * amount