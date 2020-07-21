# -*- coding: UTF-8 -*-

import sys
import os
import abc

import aiomysql

from pythinkutils.aio.mysql.ThinkAioMysql import ThinkAioMysql
from pythinkutils.common.log import g_logger
from pythinkutils.common.datetime_utils import *

class BaseUserService(object):
    @classmethod
    async def get_user(cls, nUID):
        try:
            conn_pool = await ThinkAioMysql.get_conn_pool()
            async with conn_pool.acquire() as conn:
                try:
                    async with conn.cursor(aiomysql.cursors.DictCursor) as cur:
                        await cur.execute("SELECT "
                                          "  * "
                                          "FROM "
                                          "  t_thinkauth_user "
                                          "WHERE "
                                          "  id = %s "
                                          "LIMIT 1 ", (nUID,))

                        rows = await cur.fetchall()
                        if len(rows) <= 0:
                            return None

                        return rows[0]
                except Exception as e:
                    g_logger.error(e)
                    return None
                finally:
                    conn.close()

        except Exception as e:
            g_logger.error(e)
            return None

    @classmethod
    async def get_user_id(cls, szUserName):
        try:
            conn_pool = await ThinkAioMysql.get_conn_pool()
            async with conn_pool.acquire() as conn:
                try:
                    async with conn.cursor(aiomysql.cursors.DictCursor) as cur:
                        await cur.execute("SELECT "
                                          "  id "
                                          "FROM "
                                          "  t_thinkauth_user "
                                          "WHERE "
                                          "  username = %s "
                                          "LIMIT 1 ", (szUserName,))

                        rows = await cur.fetchall()
                        if len(rows) <= 0:
                            return -1

                        return rows[0]["id"]
                except Exception as e:
                    g_logger.error(e)
                    return -1
                finally:
                    conn.close()

        except Exception as e:
            g_logger.error(e)
            return -1

    @classmethod
    async def get_user_by_username_password(cls, szUserName, szPwd):
        try:
            conn_pool = await ThinkAioMysql.get_conn_pool()
            async with conn_pool.acquire() as conn:
                try:
                    async with conn.cursor(aiomysql.cursors.DictCursor) as cur:
                        await cur.execute("SELECT "
                                          "  * "
                                          "FROM "
                                          "  t_thinkauth_user "
                                          "WHERE "
                                          "  username = %s "
                                          "  AND password = %s "
                                          "LIMIT 1 ", (szUserName, szPwd))

                        rows = await cur.fetchall()
                        if len(rows) <= 0:
                            return None

                        return rows[0]
                except Exception as e:
                    g_logger.error(e)
                    return None
                finally:
                    conn.close()

        except Exception as e:
            g_logger.error(e)
            return None

    @classmethod
    async def get_user_by_username(cls, szUsername):
        try:
            conn_pool = await ThinkAioMysql.get_conn_pool()
            async with conn_pool.acquire() as conn:
                try:
                    async with conn.cursor(aiomysql.cursors.DictCursor) as cur:
                        await cur.execute("SELECT "
                                          "  * "
                                          "FROM "
                                          "  t_thinkauth_user "
                                          "WHERE "
                                          "  username = %s "
                                          "LIMIT 1 ", (szUsername,))

                        rows = await cur.fetchall()
                        if len(rows) <= 0:
                            return None

                        return rows[0]
                except Exception as e:
                    g_logger.error(e)
                    return None
                finally:
                    conn.close()

        except Exception as e:
            g_logger.error(e)
            return None

    @classmethod
    @abc.abstractmethod
    async def create_user(cls, szUserName, szPwd, nSuperUser=0, nActive=1):
        pass

    @classmethod
    @abc.abstractmethod
    async def change_password(cls, nUID, szPwd):
        pass

    @classmethod
    @abc.abstractmethod
    async def login(cls, szUserName, szPwd):
        pass

    @classmethod
    async def check_token(cls, nUID, szToken):
        try:
            conn_pool = await ThinkAioMysql.get_conn_pool()
            async with conn_pool.acquire() as conn:
                try:
                    async with conn.cursor(aiomysql.cursors.DictCursor) as cur:
                        await cur.execute("SELECT "
                                          "  1 "
                                          "FROM "
                                          "  t_thinkauth_user_token "
                                          "WHERE "
                                          "  user_id = %s "
                                          "  AND token = %s "
                                          "  AND date_expire >= %s"
                                          "LIMIT 1 ", (nUID, szToken, get_current_time_str()))

                        rows = await cur.fetchall()
                        if len(rows) <= 0:
                            return False

                        return True
                except Exception as e:
                    g_logger.error(e)
                    return False
                finally:
                    conn.close()

        except Exception as e:
            g_logger.error(e)
            return False

    @classmethod
    async def check_token_by_username(cls, szUserName, szToken):
        nUID = await cls.get_user_id(szUserName)
        if nUID <= 0:
            return False

        bRet = await cls.check_token(nUID, szToken)
        return bRet

    @classmethod
    async def get_user_groups(cls, nUID):
        try:
            conn_pool = await ThinkAioMysql.get_conn_pool()
            async with conn_pool.acquire() as conn:
                try:
                    async with conn.cursor(aiomysql.cursors.DictCursor) as cur:
                        await cur.execute("SELECT                                                    "
                                          "	 c.*                                                     "
                                          "FROM                                                      "
                                          "	 t_thinkauth_user_group AS a                             "
                                          "	 left join t_thinkauth_user as b on a.user_id = b.id     "
                                          "	 left join t_thinkauth_group as c on a.group_id = c.id   "
                                          "where                                                     "
                                          "	 b.id = %s                                         ", (nUID,))

                        rows = await cur.fetchall()
                        if len(rows) <= 0:
                            return []

                        return rows
                except Exception as e:
                    g_logger.error(e)
                    return []
                finally:
                    conn.close()

        except Exception as e:
            g_logger.error(e)
            return []

    @classmethod
    async def get_user_groups_by_username(cls, szUser):
        try:
            conn_pool = await ThinkAioMysql.get_conn_pool()
            async with conn_pool.acquire() as conn:
                try:
                    async with conn.cursor(aiomysql.cursors.DictCursor) as cur:
                        await cur.execute("SELECT                                                    "
                                          "	 c.*                                                     "
                                          "FROM                                                      "
                                          "	 t_thinkauth_user_group AS a                             "
                                          "	 left join t_thinkauth_user as b on a.user_id = b.id     "
                                          "	 left join t_thinkauth_group as c on a.group_id = c.id   "
                                          "where                                                     "
                                          "	 b.username = %s                                         ", (szUser,))

                        rows = await cur.fetchall()
                        if len(rows) <= 0:
                            return []

                        return rows
                except Exception as e:
                    g_logger.error(e)
                    return []
                finally:
                    conn.close()

        except Exception as e:
            g_logger.error(e)
            return []

