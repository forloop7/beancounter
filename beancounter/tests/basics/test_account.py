from beancounter import Account, Deposit, Bill, Transfer, Finances
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


def test_creation_with_defaults():
    """
    Basic properties of Account constructor (with default balance).
    """
    acc = Account('Some account')

    assert acc.name() == 'Some account'
    assert acc.balance() == Decimal('0.00')


def get_test_account(name, bill=Decimal(100.00), deposit=Decimal(150.00)):
    """
    Helper method, creates a test account.
    """
    account = Account(name)
    account.bill(bill, date.today())
    account.deposit(deposit, date.today())
    return account


# TODO: Test cases where accounts are almost equal (name, balance, recorded balance, transactions, transfers)
def test_account_equality():
    """
    Accounts with the same fields are considered equal
    """

    account1 = get_test_account('account 1')
    account2 = get_test_account('account 1')

    assert account1 == account2


def test_strings():
    """
    str(account) and repr(account).
    """
    acc = get_test_account('Some acc', bill=Decimal(100.00), deposit=Decimal(150.00))

    assert str(acc) == "Account('Some acc')"
    assert repr(acc) == "Account('Some acc', balance=Decimal('50.00'))"


def test_bill_balance():
    """
    Bills can be paid from an account, updating balance.
    """
    acc = Account('Some account')

    acc.deposit(Decimal('100.00'), date.today())
    assert acc.balance() == Decimal('100.00')


def test_bill_balance2():
    """
    Bills can be paid from an account, updating balance.
    """
    acc = Account('Some account')

    acc.deposit(Decimal('100.00'), date.today())
    acc.deposit(Decimal('120.00'), date.today())
    assert acc.balance() == Decimal('220.00')


def test_deposits_list():
    """
    Deposits can be made to an account, updating balance.
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
    assert deposit1 == Deposit(amount, deposit1_date)
    assert deposit2 == Deposit(2 * amount, deposit2_date)
    assert acc.balance() == 3 * amount


def test_bills_list():
    """
    Bills can be paid from an account, updating balance.
    """
    amount = Decimal('120.00')
    acc = Account('Some account', 4 * amount)
    bill_date = date(2014, 1, 5)
    acc.bill(amount, bill_date)
    assert len(acc.transactions()) == 1

    bill = acc.transactions()[0]
    assert bill == Bill(amount, bill_date)
    assert acc.balance() == 3 * amount


def test_deposit_return():
    """
    Each deposit should return Deposit object.
    """
    acc = Account('Some account')
    amount = Decimal('150.00')
    deposit_date = date(2014, 7, 5)
    deposit = acc.deposit(amount, deposit_date)

    assert deposit == Deposit(amount, deposit_date)


def test_bill_return():
    """
    Each bill should return Bill object.
    """
    acc = Account('Some account', Decimal('200.00'))
    amount = Decimal('150.00')
    bill_date = date(2014, 7, 5)
    bill = acc.bill(amount, bill_date)

    assert bill == Bill(amount, bill_date)


def test_transfer_return():
    """
    Transfering creates proper Transfer object.
    """
    acc_from = Account('Source account')
    acc_to = Account('Target account')
    amount = Decimal('4112.11')
    tx_date = date(2001, 8, 10)
    entered = date(2001, 8, 12)
    out_recorded = date(2001, 8, 14)
    in_recorded = date(2001, 8, 19)
    transfer = acc_from.transfer(acc_to, amount, tx_date, entered, out_recorded, in_recorded)

    assert transfer == Transfer(amount, tx_date, entered, out_recorded, in_recorded)


def test_transfer_balances():
    """
    Transferring money should update balances on both sides
    """
    acc_from = Account('Source account', Decimal('500.00'))
    acc_to = Account('Target account')
    acc_from.transfer(acc_to, Decimal('100.00'), date(2014, 2, 3))

    assert acc_from.balance() == Decimal('400.00')
    assert acc_to.balance() == Decimal('100.00')


def test_deposit_recorded_balance():
    """
    Deposits made to an account must be recorded to update recorded_balance.
    """
    acc = Account('Some account')

    to_record = Decimal('100.00')
    acc.deposit(to_record, date.today())
    acc.deposit(Decimal('120.00'), date.today())
    assert acc.recorded_balance() == Decimal('0.00')

    acc.transactions()[0].record(date.today())
    assert acc.recorded_balance() == to_record


def test_bill_recorded_balance():
    """
    Bills paid from an account must be recorded to update recorded_balance.
    """
    acc = Account('Some account', Decimal('250.00'))
    bill = acc.bill(Decimal('110.00'), date.today())
    assert acc.recorded_balance() == Decimal('250.00')  # Sanity check

    bill.record(date.today())
    assert acc.recorded_balance() == Decimal('140.00')


@pytest.mark.parametrize('recorded_from,recorded_to', [(None, None),
                                                       (None, date.today()),
                                                       (date.today(), None),
                                                       (date.today(), date.today())])
def test_transfer_prerecorded_balances(recorded_from, recorded_to):
    """
    Pre-recording a Transfer should update recorded_balance on recording side
    """
    balance_from = Decimal('500.00')
    balance_to = Decimal('0.00')
    acc_from = Account('Source account', balance_from)
    acc_to = Account('Target account')
    transfer_amount = Decimal('100.00')
    acc_from.transfer(acc_to, transfer_amount, date(2014, 2, 3), None, recorded_from, recorded_to)

    if recorded_from:
        balance_from -= transfer_amount
    if recorded_to:
        balance_to += transfer_amount

    assert acc_from.recorded_balance() == balance_from
    assert acc_to.recorded_balance() == balance_to


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
    acc_from = Account('Source account', balance_from)
    acc_to = Account('Target account')
    transfer_amount = Decimal('100.00')
    transfer = acc_from.transfer(acc_to, transfer_amount, date(2014, 2, 3))

    if record_from:
        balance_from -= transfer_amount
        transfer.outgoing().record(date.today())
    if record_to:
        balance_to += transfer_amount
        transfer.incoming().record(date.today())

    assert acc_from.recorded_balance() == balance_from
    assert acc_to.recorded_balance() == balance_to


def test_finances_creation():
    """
    Confirms Finances object can be created.
    """
    acc = get_test_account('acc 1')

    assert Finances([acc]) is not None


def test_finances_equality():
    """
    Confirms Finances object can be compared.
    """
    acc1 = get_test_account('acc 1')
    acc2 = get_test_account('acc 1')

    fin1 = Finances([acc1])
    fin2 = Finances([acc2])

    assert fin1 == fin2
    assert fin1 is not fin2


def test_pickling_finances():
    """
    Finances can be pickled and unpickled.
    """
    acc1 = get_test_account('acc 1')
    fin1 = Finances([acc1])

    fin_bytes = pickle.dumps(fin1)
    fin2 = pickle.loads(fin_bytes)

    assert fin1 == fin2
    assert fin1 is not fin2