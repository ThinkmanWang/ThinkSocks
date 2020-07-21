# -*- coding: UTF-8 -*-

import sys
import os

import asyncio
import aiomysql
import aiorwlock

from pythinkutils.config.Config import *
from pythinkutils.common.log import g_logger

class ThinkAioMysql(object):
    g_dictConnPool = {}
    g_rwlock = aiorwlock.RWLock()

    @classmethod
    async def get_conn_pool_ex(cls, szGroup="mysql" ):
        ret = await cls.get_conn_pool(host=ThinkConfig.get_default_config().get(szGroup, "host")
                            , port=int(ThinkConfig.get_default_config().get(szGroup, "port"))
                            , user=ThinkConfig.get_default_config().get(szGroup, "user")
                            , password=ThinkConfig.get_default_config().get(szGroup, "password")
                            , db=ThinkConfig.get_default_config().get(szGroup, "db")
                            , mincached=int(ThinkConfig.get_default_config().get_int(szGroup, "maxconnections") / 2)
                            , maxcached=int(ThinkConfig.get_default_config().get_int(szGroup, "maxconnections"))
                            , maxconnections=int(ThinkConfig.get_default_config().get(szGroup, "maxconnections"))
                            , charset="utf8"
                            , use_unicode=True)

        return ret

    @classmethod
    async def get_conn_pool(cls
                      , host=ThinkConfig.get_default_config().get("mysql", "host")
                      , port=int(ThinkConfig.get_default_config().get("mysql", "port"))
                      , user=ThinkConfig.get_default_config().get("mysql", "user")
                      , password=ThinkConfig.get_default_config().get("mysql", "password")
                      , db=ThinkConfig.get_default_config().get("mysql", "db")
                      , mincached=int(ThinkConfig.get_default_config().get_int("mysql", "maxconnections") / 2)
                      , maxcached=int(ThinkConfig.get_default_config().get_int("mysql", "maxconnections"))
                      , maxconnections=int(ThinkConfig.get_default_config().get("mysql", "maxconnections"))
                      , charset="utf8"
                      , use_unicode=True):
        szHostPortDb = "{}:{}-{}".format(host, port, db)

        if cls.g_dictConnPool.get(szHostPortDb) is None:
            async with cls.g_rwlock.writer:
                if cls.g_dictConnPool.get(szHostPortDb) is None:
                    connPool = await aiomysql.create_pool(
                        minsize=mincached
                        , maxsize=maxcached
                        , host=host
                        , user=user
                        , password=password
                        , db=db
                        , port=port
                        , charset=charset
                        , use_unicode=use_unicode)

                    cls.g_dictConnPool[szHostPortDb] = connPool

        return cls.g_dictConnPool.get(szHostPortDb)