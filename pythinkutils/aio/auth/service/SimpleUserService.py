# -*- coding: UTF-8 -*-

import sys
import os
import uuid

from pythinkutils.aio.auth.service.BaseUserService import BaseUserService
from pythinkutils.aio.mysql.ThinkAioMysql import ThinkAioMysql
from pythinkutils.common.log import g_logger
from pythinkutils.common.datetime_utils import *

class SimpleUserService(BaseUserService):
    @classmethod
    async def create_user(cls, szUserName, szPwd, nSuperUser=0, nActive=1):
        dictUser = await cls.get_user_by_username(szUserName)
        if dictUser is not None:
            return None

        try:
            conn_pool = await ThinkAioMysql.get_conn_pool()
            async with conn_pool.acquire() as conn:
                try:
                    async with conn.cursor() as cur:
                        await cur.execute("INSERT INTO "
                                          "  t_thinkauth_user(username, password, is_superuser, is_active) "
                                          "VALUES "
                                          "  (%s, %s, %s, %s)"
                                          , (szUserName, szPwd, nSuperUser, nActive))

                        await conn.commit()

                        dictUser = await cls.get_user_by_username(szUserName)
                        return dictUser
                except Exception as e:
                    g_logger.error(e)
                    return None
                finally:
                    conn.close()
        except Exception as e:
            g_logger.error(e)
            return None

    @classmethod
    async def change_password(cls, nUID, szPwd):
        try:
            conn_pool = await ThinkAioMysql.get_conn_pool()
            async with conn_pool.acquire() as conn:
                try:
                    async with conn.cursor() as cur:
                        await cur.execute("UPDATE "
                                          "  t_thinkauth_user "
                                          "SET "
                                          "  password = %s "
                                          "WHERE "
                                          "  id = %s"
                                          , (szPwd, nUID))

                        await conn.commit()

                        dictUser = await cls.get_user(nUID)
                        return dictUser
                except Exception as e:
                    g_logger.error(e)
                    return None
                finally:
                    conn.close()
        except Exception as e:
            g_logger.error(e)
            return None

    @classmethod
    async def login(cls, szUserName, szPwd, nExpireDays=180):
        dictUser = await cls.get_user_by_username_password(szUserName, szPwd)
        if dictUser is None:
            return (-1, szUserName, None)

        # make token and insert
        szToken = str(uuid.uuid4()).replace("-", "")
        szExpire = "{} 23:59:59".format(diff_day(nExpireDays))

        try:
            conn_pool = await ThinkAioMysql.get_conn_pool()
            async with conn_pool.acquire() as conn:
                try:
                    async with conn.cursor() as cur:
                        await cur.execute("INSERT INTO "
                                          "  t_thinkauth_user_token(user_id, token, date_expire) "
                                          "VALUES "
                                          "  (%s, %s, %s)"
                                          , (dictUser["id"], szToken, szExpire))

                        await conn.commit()
                        return (dictUser["id"], szUserName, szToken)
                except Exception as e:
                    g_logger.error(e)
                    return (-1, szUserName, None)
                finally:
                    conn.close()
        except Exception as e:
            g_logger.error(e)
            return (-1, szUserName, None)