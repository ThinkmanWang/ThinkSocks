# -*- coding: UTF-8 -*-

import sys
import os
import abc
import json

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from pythinkutils.common.StringUtils import *
from pythinkutils.common.log import g_logger
from pythinkutils.common.object2json import *

class BaseAuthHandler(tornado.web.RequestHandler):

    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)

    def get_uid(self):
        return self.get_secure_cookie("uid")

    def get_username(self):
        return self.get_secure_cookie("username")

    def get_token(self):
        return self.get_secure_cookie("token")

    def get_permission_list(self):
        szPermissions = self.get_secure_cookie("permissions")
        if is_empty_string(szPermissions):
            return []

        return json.loads(szPermissions)

    def get_secure_cookie(self, szName, szDefault=None):
        byteRet = super().get_secure_cookie(szName)
        if byteRet:
            return byteRet.decode(encoding='utf-8')
        else:
            return szDefault

    def get_current_user(self):
        return {
            "uid": self.get_uid()
            , "username": self.get_username()
            , "token": self.get_token()
            , "permissions": self.get_permission_list()
        }

