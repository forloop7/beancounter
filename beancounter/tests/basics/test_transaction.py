from .test_account import get_test_account, get_test_accounts
from .test_utils import objects_equal
from beancounter import Bill, Deposit, Transfer
from decimal import Decimal
from datetime import date
import pytest

#
# # TODO: Test equality of operations from different accounts (after step 2 of refactoring should NOT be equal)


@pytest.mark.parametrize("cls", [(Bill), (Deposit)])
def test_transaction_creation(cls):
    """
    Transactions can be created
    """
    acc = get_test_account('account 1')
    amount = Decimal('12.21')
    tx_date = date(2015, 1, 5)
    entered = date(2015, 2, 2)
    recorded = date(2015, 1, 8)
    tx = cls(acc, amount, tx_date, entered)

    assert tx._amount == amount
    assert tx.date() == tx_date
    assert tx.entered() == entered
    assert len(tx.operations()) == 1
    op = tx.operations()[0]
    assert op.account() == acc
    assert op.recorded() is None


# TODO: Test cases where transactions are almost equal
@pytest.mark.parametrize("cls", [(Bill), (Deposit)])
def test_transaction_equality(cls):
    """
    Transactions with teh same type and fields are considered equal
    """
    acc = get_test_account('test 1')
    amount = Decimal('12.21')
    txdate = date(2015, 1, 5)
    entered = date(2015, 2, 2)
    recorded = date(2015, 1, 8)
    tx1 = cls(acc, amount, txdate, entered)
    tx2 = cls(acc, amount, txdate, entered)

    assert objects_equal(tx1, tx2)


@pytest.mark.parametrize("cls,amount,exp_amount", [(Bill, Decimal('32.11'), Decimal('-32.11')),
                                                   (Deposit, Decimal('43.11'), Decimal('43.11'))])
def test_transaction_balance_change(cls, amount, exp_amount):
    """
    Bill and Income have proper balance_change() implementations
    """
    logbook, acc = get_test_account('test 1')
    tx = cls(acc, amount, date.today())
    assert tx.operations()[0].balance_change() == exp_amount


@pytest.mark.parametrize("cls", [(Bill), (Deposit)])
def test_recording_transaction(cls):
    """
    Transaction can be recorded
    """
    logbook, acc = get_test_account('test 1')
    tx = cls(acc, Decimal('12.00'), date(2011, 3, 21))
    op = tx.operations()[0]
    assert op.recorded() is None

    op.record(date.today())
    assert op.recorded() == date.today()


def test_transfer_creation():
    """
    Transfers can be created
    """
    logbook, acc_from, acc_to = get_test_accounts()
    amount = Decimal('42.21')
    txdate = date(2015, 3, 5)
    entered = date(2015, 3, 2)
    tx = Transfer(acc_from, acc_to, amount, txdate, entered)

    assert tx.amount() == amount
    assert tx.date() == txdate
    assert tx.entered() == entered
    assert tx.recorded() is None
    assert tx.outgoing().recorded() is None
    assert tx.incoming().recorded() is None


# TODO: Negative equality tests for transfer


def test_transfer_equality():
    """
    Transfers with the same fields are considered equal
    """
    logbook, acc1, acc2 = get_test_accounts()
    amount = Decimal('42.21')
    txdate = date(2015, 3, 5)
    entered = date(2015, 3, 2)
    out_recorded = date(2015, 3, 8)
    in_recorded = date(2015, 3, 9)
    tx1 = Transfer(acc1, acc2, amount, txdate, entered)
    tx2 = Transfer(acc1, acc2, amount, txdate, entered)
    tx1.outgoing().record(out_recorded)
    tx2.outgoing().record(out_recorded)
    tx1.incoming().record(in_recorded)
    tx2.incoming().record(in_recorded)
    assert objects_equal(tx1, tx2)


@pytest.mark.parametrize('out_recorded,in_recorded',
                         [(None, None),
                          (date.today(), None),
                          (None, date.today()),
                          (date(2015, 1, 1), date(2015, 5, 5)),
                          (date(2015, 4, 4), date(2015, 2, 2))])
def test_transfer_side_recording(out_recorded, in_recorded):
    """
    Each side of a transfer can be recorded individually
    """
    logbook, acc1, acc2 = get_test_accounts()
    tx = Transfer(acc1, acc2, Decimal('7656.00'), date(2001, 6, 17))
    out = tx.outgoing()
    inc = tx.incoming()

    assert not tx.recorded()

    if in_recorded:
        inc.record(in_recorded)
    if out_recorded:
        out.record(out_recorded)

    assert out.recorded() == out_recorded
    assert inc.recorded() == in_recorded

    assert (tx.recorded() is not None) == (out_recorded is not None and
                                           in_recorded is not None)
