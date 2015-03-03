from beancounter import Account


comp_exclusions = { Account: [] }


def objects_equal(obj1, obj2):
    if type(obj1) is not type(obj2):
        return False

    if obj1 is None and obj2 is None:
        return True

    if type(obj1) in comp_exclusions:
        return dicts_equal(obj1.__dict__, obj2.__dict__, exclude=comp_exclusions[type(obj1)])

    return obj1 == obj2


def dicts_equal(dict1, dict2, exclude=[]):
    """
    Compares two dicts, by comparing all their values, excluding given keys.
    :param dict1: The first dict
    :param dict2: The second dict
    :param exclude: Collection of excluded keys
    :return: True or False, depending if values for non-excluded keys are same.
    """
    excl_set = set(exclude)
    key_set = set(dict1.keys()) | set(dict2.keys())
    for key in key_set - excl_set:
        try:
            if not objects_equal(dict1[key], dict2[key]):
                return False
        except KeyError:
            return False

    return True


def test_dirs_equal():
    """
    Two identical dirs should be equal
    """
    dict1 = {'a': 7, 'b': 'ala ma kota'}
    dict2 = {'a': 7, 'b': 'ala ma kota'}
    assert dicts_equal(dict1, dict2)


def test_dirs_equal_with_exclusions():
    """
    Exclusions should be honored
    """
    dict1 = {'a': 7, 'b': 'ala ma kota', 'c': 'different', 'd': 'only in this object'}
    dict2 = {'a': 7, 'b': 'ala ma kota', 'c': 'I said different', 'e': 'only here',
             'f': 'only here'}
    assert dicts_equal(dict1, dict2, exclude=['c', 'd', 'e', 'f'])


class EqTestObject:
    def __init__(self, **kw):
        for key in kw.keys():
            setattr(self, key, kw[key])


def test_objs_equal():
    """
    Verifies our test object comparator works as expected
    """
    dict1 = {'a': 7, 'b': 'ala ma kota'}
    dict2 = {'a': 7, 'b': 'ala ma kota'}

    # Forcing comparison by __dict__
    comp_exclusions[EqTestObject] = []

    assert objects_equal(EqTestObject(**dict1), EqTestObject(**dict2))


def test_objs_equal_with_exclusions():
    """
    Verifies our test object comparator works as expected
    """
    dict1 = {'a': 7, 'b': 'ala ma kota', 'c': 'different', 'd': 'only in this object'}
    dict2 = {'a': 7, 'b': 'ala ma kota', 'c': 'I said different', 'e': 'only here',
             'f': 'only here'}

    comp_exclusions[EqTestObject] = ['c', 'd', 'e', 'f']

    assert objects_equal(EqTestObject(**dict1), EqTestObject(**dict2))

