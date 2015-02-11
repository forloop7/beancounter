import beancounter
import decimal


def test_account_creation():
    """
    Basic properties of Account constructor.
    """
    account = beancounter.Account('Some account')

    assert account.name == 'Some account'
    assert account.seq == 0
    assert account.balance == decimal.Decimal('0.00')


def test_account_strings():
    """
    str(account) and repr(account)
    """
    account = beancounter.Account('Some account')

    assert str(account) == "Account(Some account)"
    assert repr(account) == "Account(Some account, seq=0, balance=Decimal('0.00'))"