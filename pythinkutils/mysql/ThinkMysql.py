# -*- coding: UTF-8 -*-

import sys
import os
import pymysql as mysql
import threading
from DBUtils.PooledDB import PooledDB

from pythinkutils.config.Config import ThinkConfig

class ThinkMysql:
    g_lock = threading.Lock()
    g_dictConnPool = {}

    @classmethod
    def get_conn_pool_ex(cls, szGroup="mysql"):
        return cls.get_conn_pool(host=ThinkConfig.get_default_config().get(szGroup, "host")
                      , port=int(ThinkConfig.get_default_config().get(szGroup, "port"))
                      , user=ThinkConfig.get_default_config().get(szGroup, "user")
                      , password=ThinkConfig.get_default_config().get(szGroup, "password")
                      , db=ThinkConfig.get_default_config().get(szGroup, "db")
                      , mincached=int(ThinkConfig.get_default_config().get_int(szGroup, "maxconnections") / 2)
                      , maxcached=int(ThinkConfig.get_default_config().get_int(szGroup, "maxconnections"))
                      , maxconnections=int(ThinkConfig.get_default_config().get(szGroup, "maxconnections"))
                      , charset="utf8"
                      , use_unicode=True)

    @classmethod
    def get_conn_pool(cls
                      , host=ThinkConfig.get_default_config().get("mysql", "host")
                      , port=int(ThinkConfig.get_default_config().get("mysql", "port"))
                      , user=ThinkConfig.get_default_config().get("mysql", "user")
                      , password=ThinkConfig.get_default_config().get("mysql", "password")
                      , db=ThinkConfig.get_default_config().get("mysql", "db")
                      , mincached = int(ThinkConfig.get_default_config().get_int("mysql", "maxconnections") / 2)
                      , maxcached = int(ThinkConfig.get_default_config().get_int("mysql", "maxconnections"))
                      , maxconnections=int(ThinkConfig.get_default_config().get("mysql", "maxconnections"))
                      , charset = "utf8"
                      , use_unicode = True):

        szHostPortDb = "{}:{}-{}".format(host, port, db)

        if cls.g_dictConnPool.get(szHostPortDb) is None:
            with cls.g_lock:
                if cls.g_dictConnPool.get(szHostPortDb) is None:

                    conn_pool = PooledDB(mysql
                                         , mincached = mincached
                                         , maxcached = maxcached
                                         , host=host
                                         , user=user
                                         , password=password
                                         , db=db
                                         , port=port
                                         , maxconnections=maxconnections
                                         , charset = charset
                                         , use_unicode = use_unicode)

                    cls.g_dictConnPool[szHostPortDb] = conn_pool


        return cls.g_dictConnPool.get(szHostPortDb)
