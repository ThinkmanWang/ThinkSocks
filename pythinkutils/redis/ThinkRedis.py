# -*- coding: UTF-8 -*-

import sys
import os

import redis
import threading

from pythinkutils.config.Config import *

class ThinkRedis(object):
    g_lock = threading.Lock()
    g_dictConnPool = {}

    @classmethod
    def get_conn_pool_ex(cls, szGroup="redis"):
        return cls.get_conn_pool(host=g_config.get(szGroup, "host")
                                 , password=g_config.get(szGroup, "password")
                                 , port=int(g_config.get(szGroup, "port"))
                                 , db=int(g_config.get(szGroup, "db"))
                                 , max_connections=int(g_config.get(szGroup, "max_connections")))

    @classmethod
    def get_conn_pool(cls, host=g_config.get("redis", "host")
                      , password=g_config.get("redis", "password")
                      , port=int(g_config.get("redis", "port"))
                      , db=int(g_config.get("redis", "db"))
                      , max_connections = int(g_config.get("redis", "max_connections"))):
        szHostPortDb = "{}:{}-{}".format(host, port, db)

        if cls.g_dictConnPool.get(szHostPortDb) is None:
            with cls.g_lock:
                if cls.g_dictConnPool.get(szHostPortDb) is None:
                    kwargs = {
                        'host': host,
                        'port': port,
                        'db': db,
                        'max_connections': max_connections,
                        'password': password,
                    }

                    conn_pool = redis.ConnectionPool(**kwargs)

                    cls.g_dictConnPool[szHostPortDb] = conn_pool

        return cls.g_dictConnPool.get(szHostPortDb)