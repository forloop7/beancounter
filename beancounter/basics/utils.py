def are_equal(dict1, dict2, exclude=[]):
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
            if dict1[key] != dict2[key]:
                return False
        except KeyError:
            return False

    return True