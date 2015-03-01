from beancounter.basics.utils import are_equal


def test_dirs_equal():
    """
    Two identical dirs should be equal
    """
    dict1 = {'a': 7, 'b': 'ala ma kota'}
    dict2 = {'a': 7, 'b': 'ala ma kota'}
    assert are_equal(dict1, dict2)


def test_dirs_equal_with_exclusions():
    """
    Exclusions should be honored
    """
    dict1 = {'a': 7, 'b': 'ala ma kota', 'c': 'different', 'd': 'only in this object'}
    dict2 = {'a': 7, 'b': 'ala ma kota', 'c': 'I said different', 'e': 'only here',
             'f': 'only here'}
    assert are_equal(dict1, dict2, exclude=['c', 'd', 'e', 'f'])