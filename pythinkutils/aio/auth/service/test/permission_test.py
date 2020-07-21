# -*- coding: UTF-8 -*-

import sys
import os

import asyncio

from pythinkutils.aio.auth.service.PermissionService import PermissionService

from pythinkutils.common.object2json import *
from pythinkutils.common.log import g_logger

async def test_create_permission():
    await PermissionService.create_permission("permission_read_user_info")

    dictPermission = await PermissionService.select_permission("permission_read_user_info")
    g_logger.info(dictPermission)

    await PermissionService.grant_permission_to_user(dictPermission["id"], 10000001)
    await PermissionService.grant_permission_to_group(dictPermission["id"], 10000001)

async def test_has_permission():
    dictPermission = await PermissionService.select_permission("permission_read_user_info")
    bHasPermission = await PermissionService.user_has_permission(10000001, dictPermission["id"])
    g_logger.info(bHasPermission)

async def group_has_permission():
    dictPermission = await PermissionService.select_permission("permission_read_user_info")

    bHasPermission = await PermissionService.group_has_permission(10000001, dictPermission["id"])
    g_logger.info(bHasPermission)

async def test():
    await test_create_permission()
    await test_has_permission()
    await group_has_permission()

def main():
    loop = asyncio.get_event_loop()

    asyncio.gather(test())

    loop.run_forever()

if __name__ == '__main__':
    main()