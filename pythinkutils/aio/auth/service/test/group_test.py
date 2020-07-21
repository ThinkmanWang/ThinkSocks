# -*- coding: UTF-8 -*-

import sys
import os

import asyncio

from pythinkutils.aio.auth.service.GroupService import GroupService
from pythinkutils.common.object2json import *
from pythinkutils.common.log import g_logger

async def test_get_group():
    dictRet = await GroupService.get_group_by_name("admin")
    if dictRet is None:
        g_logger.info("FXXK")
        return

    g_logger.info(obj2json(dictRet))


async def test_create_group():
    dictRet = await GroupService.create_group("FXXK3")
    if dictRet is None:
        g_logger.info("FXXK Failed")
        return

    g_logger.info(obj2json(dictRet))

    ret = await GroupService.add_user_to_group(10000008, dictRet["id"])
    g_logger.info(ret)


async def test():
    await test_get_group()
    await test_create_group()

def main():
    # await test_query_user_by_name()
    loop = asyncio.get_event_loop()

    asyncio.gather(test())

    loop.run_forever()

if __name__ == '__main__':
    main()