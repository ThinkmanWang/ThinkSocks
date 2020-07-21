# -*- coding: UTF-8 -*-

import sys
import os

import hashlib

class MD5Utils(object):

    @classmethod
    def md5(cls, szText):
        m = hashlib.md5()
        m.update(szText.encode("utf8"))
        # print(m.hexdigest())
        return m.hexdigest()

    @classmethod
    def md5_file(cls, szFilePath):
        if not os.path.isfile(szFilePath):
            return ""

        myhash = hashlib.md5()
        f = open(szFilePath, 'rb')

        while True:
            b = f.read(8096)
            if not b:
                break

            myhash.update(b)

        f.close()
        return myhash.hexdigest()


# print(MD5Utils.md5("123456").lower())
# print(MD5Utils.md5_file("log.py"))
