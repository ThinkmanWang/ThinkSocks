# -*- coding: UTF-8 -*-

import sys
import os

import asyncio
import aioredis
import aiorwlock

from pythinkutils.config.Config import *
from pythinkutils.common.datetime_utils import *
from pythinkutils.common.log import g_logger

class ThinkAioRedisPool(object):

    g_dictConnPool = {}
    g_rwlock = aiorwlock.RWLock()

    @classmethod
    async def get_conn_pool_ex(cls, szGroup="redis"):
        ret = await cls.get_conn_pool(host=ThinkConfig.get_default_config().get(szGroup, "host")
                            , password=ThinkConfig.get_default_config().get(szGroup, "password")
                            , port=ThinkConfig.get_default_config().get_int(szGroup, "port")
                            , db=ThinkConfig.get_default_config().get_int(szGroup, "db")
                            , max_connections=int(ThinkConfig.get_default_config().get_int(szGroup, "max_connections")))

        return ret

    @classmethod
    async def get_conn_pool(cls
                            , host=ThinkConfig.get_default_config().get("redis", "host")
                            , password=ThinkConfig.get_default_config().get("redis", "password")
                            , port=ThinkConfig.get_default_config().get_int("redis", "port")
                            , db=ThinkConfig.get_default_config().get_int("redis", "db")
                            , max_connections=int(ThinkConfig.get_default_config().get_int("redis", "max_connections"))):

        szHostPortDb = "{}:{}-{}".format(host, port, db)
        if cls.g_dictConnPool.get(szHostPortDb) is None:

            async with cls.g_rwlock.writer:
                if cls.g_dictConnPool.get(szHostPortDb) is None:
                    connPool = await cls.mk_conn_pool(host, password, port, db, max_connections)

                    cls.g_dictConnPool[szHostPortDb] = connPool

        return cls.g_dictConnPool.get(szHostPortDb)

    @classmethod
    async def mk_conn_pool(cls
                     , host='127.0.0.1'
                     , password=None
                     , port=6379
                     , db=0
                     , max_connections=16):

        szAddress = "redis://{}:{}".format(host, port)
        _conn_pool = await aioredis.create_pool(szAddress, db=db, password=password, minsize=2, maxsize=max_connections)
        return _conn_pool


# async def main():
#     # conn_pool = await ThinkAioRedisPool.get_default_conn_pool()
#     with await (await ThinkAioRedisPool.get_conn_pool_ex()) as conn:
#         await conn.execute('set', 'fxxxxk', get_current_time_str())
#
#         szVal = await conn.execute("get", "fxxxxk")
#         print("return val: ", szVal.decode())
#
# if __name__ == '__main__':
#     asyncio.get_event_loop().run_until_complete(main())