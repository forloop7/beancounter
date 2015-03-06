from beancounter import Account, Deposit, Bill, Transfer, Logbook
from .test_utils import objects_equal
from decimal import Decimal
from datetime import date
import pytest
import pickle


def test_creation():
    """
    Basic properties of Account constructor.
    """
    balance = Decimal('123.02')
    acc = Account('Some account', balance)

    assert acc.name() == 'Some account'
    assert acc.balance() == balance


def get_test_account(name='test account', balance=Decimal('0.00'), logbook=None):
    """
    Helper method, creates a test account.
    """
    if not logbook:
        logbook = Logbook()
    return logbook, logbook.add_account(name, balance=balance)


def get_test_accounts(name1='test account 1', name2='test account 2', 
                      balance1=Decimal('0.00'), balance2=Decimal('0.00'), logbook=None):
    """
    Helper method, creates a test account.
    """
    logbook, acc1 = get_test_account(name1, balance=balance1, logbook=logbook)
    logbook, acc2 = get_test_account(name2, balance=balance2, logbook=logbook)
    return (logbook, acc1, acc2)


def get_busy_test_account(name, bill=Decimal('100.00'), deposit=Decimal('150.00'), logbook=None):
    """
    Helper method, creates a test account.
    """
    (logbook, account) = get_test_account(name, logbook=logbook)
    logbook.bill(account, bill, date.today())
    logbook.deposit(account, deposit, date.today())
    return (logbook, account)


def test_strings():
    """
    str(account) and repr(account).
    """
    _, acc = get_busy_test_account('Some acc', deposit=Decimal(150.00), bill=Decimal(100.00))

    assert str(acc) == "Account('Some acc')"
    assert repr(acc) == "Account('Some acc', balance=Decimal('50.00'))"


def test_bill_balance():
    """
    Bills can be paid from an account, updating balance.
    """
    logbook, acc = get_test_account('Some account', balance=Decimal('1000.00'))

    logbook.bill(acc, Decimal('100.00'), date.today())
    logbook.bill(acc, Decimal('120.00'), date.today())
    assert acc.balance() == Decimal('780.00')


def test_deposit_balance():
    """
    Deposits can be made to an account, updating balance.
    """
    logbook, acc = get_test_account('Some account')

    logbook.deposit(acc, Decimal('100.00'), date.today())
    logbook.deposit(acc, Decimal('120.00'), date.today())
    assert acc.balance() == Decimal('220.00')


def test_deposits_list():
    """
    Deposits can be made to an account, updating balance.
    """
    logbook, acc = get_test_account('Some account')
    amount = Decimal('120.00')
    deposit1_date = date(2014, 1, 5)
    deposit2_date = date(2014, 2, 5)
    logbook.deposit(acc, amount, deposit1_date)
    logbook.deposit(acc, 2 * amount, deposit2_date)
    assert len(logbook.transactions()) == 2

    deposit1 = logbook.transactions()[0]
    deposit2 = logbook.transactions()[1]
    assert objects_equal(deposit1, Deposit(acc, amount, deposit1_date))
    assert objects_equal(deposit2, Deposit(acc, 2 * amount, deposit2_date))
    assert acc.balance() == 3 * amount


def test_bills_list():
    """
    Bills can be paid from an account, updating balance.
    """
    amount = Decimal('120.00')
    logbook, acc = get_test_account('Some account', balance=4*amount)
    bill_date = date(2014, 1, 5)
    logbook.bill(acc, amount, bill_date)
    assert len(logbook.transactions()) == 1

    bill = logbook.transactions()[0]
    assert objects_equal(bill, Bill(acc, amount, bill_date))
    assert acc.balance() == 3 * amount


def test_deposit_return():
    """
    Each deposit should return Deposit object.
    """
    logbook, acc = get_test_account('Some account')
    amount = Decimal('150.00')
    deposit_date = date(2014, 7, 5)
    deposit = logbook.deposit(acc, amount, deposit_date)

    assert objects_equal(deposit, Deposit(acc, amount, deposit_date))


def test_bill_return():
    """
    Each bill should return Bill object.
    """
    logbook, acc = get_test_account('Some account', balance=Decimal('200.00'))
    amount = Decimal('150.00')
    bill_date = date(2014, 7, 5)
    bill = logbook.bill(acc, amount, bill_date)

    assert objects_equal(bill, Bill(acc, amount, bill_date))


def test_deposit_recorded_balance():
    """
    Deposits made to an account must be recorded to update recorded_balance.
    """
    logbook, acc = get_test_account('Some account')

    amt_to_record = Decimal('100.00')
    to_record = logbook.deposit(acc, amt_to_record, date.today())
    logbook.deposit(acc, Decimal('120.00'), date.today())
    assert acc.recorded_balance() == Decimal('0.00')

    to_record.operations()[0].record(date.today())
    assert acc.recorded_balance() == amt_to_record


def test_bill_recorded_balance():
    """
    Bills paid from an account must be recorded to update recorded_balance.
    """
    logbook, acc = get_test_account('Some account', balance=Decimal('250.00'))
    bill = logbook.bill(acc, Decimal('110.00'), date.today())
    assert acc.recorded_balance() == Decimal('250.00')  # Sanity check

    bill.operations()[0].record(date.today())
    assert acc.recorded_balance() == Decimal('140.00')


def test_transfer_return():
    """
    Transfering creates proper Transfer object.
    """
    logbook, acc_from, acc_to = get_test_accounts()
    amount = Decimal('4112.11')
    tx_date = date(2001, 8, 10)
    entered = date(2001, 8, 12)
    transfer = logbook.transfer(acc_from, acc_to, amount, tx_date, entered)

    assert objects_equal(transfer, Transfer(acc_from, acc_to, amount, tx_date, entered))


def test_transfer_balances():
    """
    Transferring money should update balances on both sides
    """
    logbook, acc_from, acc_to = get_test_accounts(balance1=Decimal('500.00'))
    transfer = logbook.transfer(acc_from, acc_to, Decimal('100.00'), date(2014, 2, 3))

    assert acc_from.balance() == Decimal('400.00')
    assert acc_to.balance() == Decimal('100.00')


@pytest.mark.parametrize('record_from,record_to', [(False, False),
                                                   (False, True),
                                                   (True, False),
                                                   (True, True)])
def test_transfer_recorded_balances(record_from, record_to):
    """
    Recording a TransferSide should update recorded_balance on recording side
    """
    balance_from = Decimal('500.00')
    balance_to = Decimal('0.00')
    logbook, acc_from, acc_to = get_test_accounts(balance1=balance_from)
    transfer_amount = Decimal('100.00')
    transfer = logbook.transfer(acc_from, acc_to, transfer_amount, date(2014, 2, 3))

    if record_from:
        balance_from -= transfer_amount
        transfer.outgoing().record(date.today())
    if record_to:
        balance_to += transfer_amount
        transfer.incoming().record(date.today())

    assert acc_from.recorded_balance() == balance_from
    assert acc_to.recorded_balance() == balance_to


def test_logbook_equality():
    """
    Confirms Logbook object can be compared.
    """
    logbook1, acc1 = get_busy_test_account('acc 1')
    logbook2, acc2 = get_busy_test_account('acc 1')

    assert objects_equal(logbook1, logbook2)
    assert logbook1 is not logbook2


# TODO: Test logbook inequality
#       - different number of accounts
#       - different account name
#       - recorded/not recorded transaction
#       - different transactions (amount, date, entered_date)


def test_pickling_logbook():
    """
    Logbook can be pickled and unpickled.
    """
    logbook1, acc1 = get_busy_test_account('acc 1')

    logbook_bytes = pickle.dumps(logbook1)
    logbook2 = pickle.loads(logbook_bytes)

    assert objects_equal(logbook1, logbook2)
    assert logbook1 is not logbook2
