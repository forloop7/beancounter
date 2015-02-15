from beancounter.basics.transaction import Transaction
from beancounter import Bill, Deposit, Transfer
from decimal import Decimal
from datetime import date
import pytest


@pytest.mark.parametrize("cls", [(Transaction), (Bill), (Deposit)])
def test_transaction_creation(cls):
    """Transactions can be created"""
    amount = Decimal('12.21')
    txdate = date(2015, 1, 5)
    entered = date(2015, 2, 2)
    recorded = date(2015, 1, 8)
    tx = cls(amount, txdate, entered, recorded)

    assert tx.amount() == amount
    assert tx.date() == txdate
    assert tx.entered() == entered
    assert tx.is_recorded() == True
    assert tx.recorded() == recorded


@pytest.mark.parametrize("cls", [(Transaction), (Bill), (Deposit)])
def test_transaction_creation_defaults(cls):
    """Transactions can be created with proper defaults"""
    amount = Decimal('1211.21')
    txdate = date(2015, 2, 5)
    tx = cls(amount, txdate)

    assert tx.amount() == amount
    assert tx.date() == txdate
    assert tx.entered() == date.today()
    assert tx.is_recorded() == False
    assert tx.recorded() is None


@pytest.mark.parametrize("cls,amount,exp_amount", [(Bill, Decimal('32.11'), Decimal('-32.11')),
                                                   (Deposit, Decimal('43.11'), Decimal('43.11'))])
def test_transaction_balance_change(cls, amount, exp_amount):
    """Bill and Income have proper balance_change() implementations"""
    tx = cls(amount, date.today())

    assert tx.balance_change() == exp_amount


def test_transfer_creation():
    """Transfers can be created"""
    amount = Decimal('42.21')
    txdate = date(2015, 3, 5)
    entered = date(2015, 3, 2)
    in_recorded = date(2015, 3, 9)
    out_recorded = date(2015, 3, 8)
    tx = Transfer(amount, txdate, entered, out_recorded, in_recorded)

    assert tx.amount() == amount
    assert tx.date() == txdate
    assert tx.entered() == entered
    assert tx.is_recorded()
    assert tx.recorded() == max(in_recorded, out_recorded)
    assert tx.outgoing().recorded() == out_recorded
    assert tx.incoming().recorded() == in_recorded


def test_transfer_creation_default():
    """Transfers can be created with defaults"""
    amount = Decimal('42.21')
    txdate = date(2015, 3, 5)
    entered = date(2015, 3, 2)
    tx = Transfer(amount, txdate, entered)

    assert tx.amount() == amount
    assert tx.date() == txdate
    assert tx.entered() == entered
    assert not tx.is_recorded()
    assert tx.recorded() is None
    assert tx.outgoing().recorded() is None
    assert tx.incoming().recorded() is None


@pytest.mark.parametrize('in_recorded,out_recorded,exp_recorded',
                         [(None, None, None),
                          (date.today(), None, None),
                          (None, date.today(), None),
                          (date(2015, 1, 1), date(2015, 5, 5), date(2015, 5, 5)),
                          (date(2015, 4, 4), date(2015, 2, 2), date(2015, 4, 4))])
def test_transfer_recording(in_recorded, out_recorded, exp_recorded):
    """Transfers are recorded when both sides are recorded"""
    amount = Decimal('42.21')
    txdate = date(2015, 3, 5)
    entered = date(2015, 3, 2)
    tx = Transfer(amount, txdate, entered, in_recorded, out_recorded)

    assert tx.is_recorded() == (exp_recorded is not None)
    assert tx.recorded() == exp_recorded


def test_transfer_sides():
    """Transfer in and out have correct balances"""
    amount = Decimal('1211.21')
    txdate = date(2015, 2, 5)
    tx = Transfer(amount, txdate)
    inc = tx.incoming()
    out = tx.outgoing()

    assert tx.amount() == inc.amount() == out.amount()
    assert tx.date() == inc.date() == out.date()
    assert tx.entered() == inc.entered() == out.entered()
    assert tx.amount() == inc.balance_change() == -out.balance_change()
