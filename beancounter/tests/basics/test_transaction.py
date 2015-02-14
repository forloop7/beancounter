from beancounter.basics.transaction import Transaction
from beancounter import Bill, Deposit
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

    assert tx.amount == amount
    assert tx.date == txdate
    assert tx.entered == entered
    assert tx.recorded == recorded


@pytest.mark.parametrize("cls", [(Transaction), (Bill), (Deposit)])
def test_transaction_creation_defaults(cls):
    """Transactions can be created with proper defaults"""
    amount = Decimal('1211.21')
    txdate = date(2015, 2, 5)
    tx = cls(amount, txdate)

    assert tx.amount == amount
    assert tx.date == txdate
    assert tx.entered == date.today()
    assert tx.recorded == None


@pytest.mark.parametrize("cls,amount,exp_amount", [(Bill, Decimal('32.11'), Decimal('-32.11')),
                                                   (Deposit, Decimal('43.11'), Decimal('43.11'))])
def test_transaction_balance_change(cls, amount, exp_amount):
    """Bill and Income have proper balance_change() implementations"""
    tx = cls(amount, date.today())

    assert tx.balance_change() == exp_amount