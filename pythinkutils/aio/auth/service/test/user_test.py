# -*- coding: UTF-8 -*-

import sys
import os

import asyncio

from pythinkutils.aio.auth.service.SimpleUserService import SimpleUserService
from pythinkutils.common.object2json import *
from pythinkutils.common.log import g_logger

async def test_create_user():
    szUsername = "thinkman004"
    szPwd = "Ab123456"

    dictRet = await SimpleUserService.create_user(szUsername, szPwd)
    g_logger.info(dictRet)

    ret = await SimpleUserService.login(szUsername, szPwd)
    g_logger.info(ret)

async def test_user_token():
    ret = await SimpleUserService.check_token(10000008, "85b06a75bf6b4e0aa0d759dabb457130")
    g_logger.info(ret)

async def test_login():
    szUsername = "thinkman004"
    szPwd = "Ab123456"

    ret = await SimpleUserService.login(szUsername, szPwd)
    g_logger.info(ret)

async def test():
    await test_user_token()
    # await test_create_user()
    await test_login()

def main():
    # await test_query_user_by_name()
    loop = asyncio.get_event_loop()

    asyncio.gather(test())

    loop.run_forever()

if __name__ == '__main__':
    main()