# -*- coding: UTF-8 -*-

import sys
import os

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado import gen
import aiomysql

from tornado.httpserver import HTTPServer
from tornado.platform.asyncio import AsyncIOMainLoop
import asyncio

from pythinkutils.common.log import g_logger
from pythinkutils.aio.auth.tornado.handler.BaseSimpleAuthHandler import *
from pythinkutils.aio.auth.tornado.handler.ThinkLoginHandler import ThinkLoginHandler
from pythinkutils.common.StringUtils import *

class LogoutHandler(BaseSimpleAuthHandler):
    async def post(self):
        await self.logout()
        self.redirect("/login")

    async def get(self):
        await self.post()

class FxxkHandler(BaseSimpleAuthHandler):

    async def on_goto_login_page(self):
        g_logger.info("Goto login page")
        self.redirect("/login?redirect_url=%2ffxxk")

    @page_permission_required("permission_hehe")
    async def get(self):
        self.write("FxxkHandler To be continued...")

class MainHandler(BaseSimpleAuthHandler):

    @page_login_required()
    async def get(self):
        self.write("HOMEPAGE To be continued...")

class ApiHandler(BaseSimpleAuthHandler):
    @api_login_required()
    async def post(self):
        self.write('''{"code": 0, "msg": "ApiHandler success"}''')

    @api_login_required()
    async def get(self):
        await self.post()


class AnotherApiHandler(BaseSimpleAuthHandler):
    @api_permission_required("permission_hehe")
    async def post(self):
        self.write('''{"code": 0, "msg": "AnotherApiHandler success"}''')

    @api_permission_required("permission_hehe")
    async def get(self):
        await self.post()


application = tornado.web.Application(handlers = [
    (r"/login", ThinkLoginHandler)
    , (r"/fxxk", FxxkHandler)
    , (r"/api1.json", ApiHandler)
    , (r"/api2.json", AnotherApiHandler)
    , (r'/', MainHandler)
    , (r"/logout", LogoutHandler)
], cookie_secret="BUEa2ckrQtmBofim3aP6cwr/acg0LEu6mHUxq4O3EY0=", autoreload=False)

"""
>>> import base64
>>> import uuid
>>> print base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)
BUEa2ckrQtmBofim3aP6cwr/acg0LEu6mHUxq4O3EY0=

"""

async def func1():
    return "Server Started"
async def on_server_started():
    szMsg = await func1()
    g_logger.info(szMsg)

if __name__ == '__main__':

    http_server = HTTPServer(application)
    http_server.bind(8590)
    http_server.start(0)

    # ipDB = IPLocation.instance()
    g_logger.info('HTTP Server started... %d' % (os.getpid(),))
    asyncio.gather(on_server_started())

    tornado.ioloop.IOLoop.current().start()

    # tornado.platform.asyncio.AsyncIOMainLoop().install()
    # AsyncIOMainLoop().install()
    # ioloop = asyncio.get_event_loop()
    #
    # asyncio.gather(on_server_started())
    #
    # ioloop.run_forever()