# -*- coding: utf-8 -*-

import string
from random import choice


def is_empty_string(szStr):
    try:
        if szStr is None or 0 == len(szStr.strip()):
            return True
        else:
            return False
    except Exception as e:
        return True

def random_password(length=8,chars=string.ascii_letters+string.digits):
    return ''.join([choice(chars) for i in range(length)])


# print is_empty_string(180)
# print is_empty_string("180")