# -*- coding: UTF-8 -*-

import sys
import os
import abc

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from pythinkutils.common.StringUtils import *
from pythinkutils.common.log import g_logger
from pythinkutils.aio.auth.tornado.handler.BaseAuthHandler import BaseAuthHandler

class BaseSimpleAuthHandler(BaseAuthHandler):

    async def on_api_user_not_login(self):
        self.write('''{"code": 1024, "msg": "Login required"}''')

    async def on_api_permission_denied(self):
        self.write('''{"code": 1025, "msg": "Permission Denied"}''')

    # @abc.abstractmethod
    async def on_goto_login_page(self):
        g_logger.info("Goto login page")
        self.redirect("/login")

    async def login(self, szUsername, szPwd):
        from pythinkutils.aio.auth.service.SimpleUserService import SimpleUserService
        from pythinkutils.aio.auth.service.PermissionService import PermissionService
        from pythinkutils.common.object2json import obj2json

        nExpireDays = 180

        nUID, _szUsername, szToken = await SimpleUserService.login(szUsername, szPwd, nExpireDays)
        if is_empty_string(szToken):
            return (nUID, _szUsername, szToken)

        self.set_secure_cookie("uid", "{}".format(nUID), expires_days=nExpireDays)
        self.set_secure_cookie("username", _szUsername, expires_days = nExpireDays)
        self.set_secure_cookie("token", szToken, expires_days = nExpireDays)

        lstPermissions = await PermissionService.my_permission_list(nUID)
        self.set_secure_cookie("permissions", obj2json(lstPermissions), expires_days = nExpireDays)

        return (nUID, _szUsername, szToken)

    async def logout(self):
        self.clear_cookie("uid")
        self.clear_cookie("username")
        self.clear_cookie("token")
        self.clear_cookie("permissions")

def api_login_required():
    def auth_decorator(func):
        async def inner(self, *args, **kwargs):
            from pythinkutils.aio.auth.service.SimpleUserService import SimpleUserService

            if is_empty_string(self.get_argument("uid", "")) \
                    or is_empty_string(self.get_argument("token", "")):
                await self.on_api_user_not_login()
            else:
                bTokenValid = await SimpleUserService.check_token(int(self.get_argument("uid", "-1")), self.get_argument("token", ""))
                if bTokenValid:
                    await func(self, *args, **kwargs)
                else:
                    await self.on_api_user_not_login()
        return inner
    return auth_decorator

def api_permission_required(szPermission):
    def auth_decorator(func):
        async def inner(self, *args, **kwargs):
            from pythinkutils.aio.auth.service.PermissionService import PermissionService
            from pythinkutils.aio.auth.service.SimpleUserService import SimpleUserService

            nUID = int(self.get_argument("uid", "-1"))
            szToken = self.get_argument("token", "")

            if nUID < 0 or is_empty_string(szToken):
                await self.on_api_user_not_login()
                return

            bTokenValid = await SimpleUserService.check_token(int(self.get_argument("uid", "-1")), self.get_argument("token", ""))
            if False == bTokenValid:
                await self.on_api_user_not_login()
                return

            dictPermission = await PermissionService.select_permission(szPermission)
            if dictPermission is None or False == dictPermission.get("name"):
                await self.on_api_permission_denied()

            bHasPermission = await PermissionService.user_has_permission(nUID, dictPermission["id"])
            if bHasPermission:
                await func(self, *args, **kwargs)
            else:
                await self.on_api_permission_denied()

        return inner
    return auth_decorator

def page_login_required():
    def auth_decorator(func):
        async def inner(self, *args, **kwargs):
            from pythinkutils.aio.auth.service.SimpleUserService import SimpleUserService

            if is_empty_string(self.get_secure_cookie("uid")) \
                    or is_empty_string(self.get_secure_cookie("username")) \
                    or is_empty_string(self.get_secure_cookie("token")):
                await self.on_goto_login_page()
            else:
                bTokenValid = await SimpleUserService.check_token(int(self.get_secure_cookie("uid", "-1")), self.get_secure_cookie("token", ""))
                if bTokenValid:
                    await func(self, *args, **kwargs)
                else:
                    await self.on_goto_login_page()
        return inner
    return auth_decorator

def page_permission_required(szPermission):
    def auth_decorator(func):
        async def inner(self, *args, **kwargs):
            from pythinkutils.aio.auth.service.PermissionService import PermissionService
            from pythinkutils.aio.auth.service.SimpleUserService import SimpleUserService

            nUID = int(self.get_secure_cookie("uid", "-1"))
            szUser = self.get_secure_cookie("username", "")
            szToken = self.get_secure_cookie("token", "")

            if nUID < 0 or is_empty_string(szUser) or is_empty_string(szToken):
                await self.on_goto_login_page()
                return

            bTokenValid = await SimpleUserService.check_token(nUID, szToken)
            if False == bTokenValid:
                await self.on_goto_login_page()
                return

            dictPermission = await PermissionService.select_permission(szPermission)
            if dictPermission is None or False == dictPermission.get("name"):
                await self.on_goto_login_page()

            bHasPermission = await PermissionService.user_has_permission(nUID, dictPermission["id"])
            if bHasPermission:
                await func(self, *args, **kwargs)
            else:
                await self.on_goto_login_page()

        return inner
    return auth_decorator
