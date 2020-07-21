# -*- coding: UTF-8 -*-

import sys
import os
import re

class RegularUtils(object):
    @classmethod
    def is_phone(cls, szVal):
        return None != re.match("^1[0-9][0-9]{9}$", szVal)

    @classmethod
    def is_email(cls, szVal):
        return None != re.match("^[a-zA-Z]\w{5,10}@([0-9a-zA-Z]{3,5}\.){1,3}[a-z]{3}$", szVal)


# print(RegularUtils.is_phone("12334341"))
# print(RegularUtils.is_phone("19921675203"))
# print(RegularUtils.is_phone("18621675203"))
# print(RegularUtils.is_email("wangxf1985@gmail.com"))
# print(RegularUtils.is_email("www.baidu.com"))