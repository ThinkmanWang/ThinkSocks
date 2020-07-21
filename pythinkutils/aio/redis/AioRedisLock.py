# -*- coding: UTF-8 -*-

import sys
import os
import uuid
import time

import asyncio

from pythinkutils.common.datetime_utils import *
from pythinkutils.common.StringUtils import *

class AioRedisLock(object):

    @classmethod
    def mk_key(cls, szName):
        return "lock:" + szName

    @classmethod
    async def acquire(cls, conn=None, lockname='', acquire_timeout=10):
        szVal = await cls.acquire_with_timeout(conn, lockname, acquire_timeout)
        return szVal

    @classmethod
    async def acquire_with_timeout(cls, conn=None, lockname='', acquire_timeout=10, lock_timeout=60):
        if conn is None:
            return None

        szID = await cls.acquire(conn, lockname, acquire_timeout)
        if is_empty_string(szID):
            return None

        try:
            conn.execute("EXPIRE", cls.mk_key(lockname), lock_timeout)
        except Exception as e:
            pass

        return szID

    @classmethod
    async def release(cls, conn=None, lockname='', identifier=''):
        if conn is None:
            return False

        szKey = cls.mk_key(lockname)

        try:
            szVal = await conn.execute("GET", szKey)
            if bytes == type(szVal):
                szVal = szVal.decode(encoding='utf-8')
            if is_empty_string(szVal):
                return False

            if szVal != identifier:
                return False

            await conn.execute("DEL", szKey)

            return True
        except Exception as e:
            return False


# async def main():
#     from aiothinkutils.redis.ThinkAioRedisPool import ThinkAioRedisPool
#     with await (await ThinkAioRedisPool.get_default_conn_pool()) as conn:
#         szVal = await AioRedisLock.acquire_with_timeout(conn, "lock_test", 10)
#         print(szVal)
#
#         szVal1 = await AioRedisLock.acquire_with_timeout(conn, "lock_test", 10)
#         print(szVal1)
#
#         await asyncio.sleep(5)
#         print("Delete lock")
#         await AioRedisLock.release(conn, "lock_test", szVal)
#
# if __name__ == '__main__':
#     asyncio.run(main())