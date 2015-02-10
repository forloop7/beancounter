import beancounter

def test_account_creation():
    account = beancounter.Account('Some account')
    assert account.name == 'Some account'