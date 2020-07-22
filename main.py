# -*- coding: utf-8 -*-

import sys
import os
import asyncio

import tornado.ioloop
import tornado
import tornado.process

from tornado.tcpserver import TCPServer
from tornado.iostream import StreamClosedError
from tornado import gen
from tornado.platform.asyncio import AsyncIOMainLoop
from tornado.netutil import *

def main():
    # server = ThinkSocks()
    # server.listen(8530)
    # g_logger.info("Server Started!!!")
    # tornado.ioloop.IOLoop.instance().start()

    # multiple sub-process
    # server = ThinkSocks()
    # server.bind(8530)
    # server.start(0)  # Forks multiple sub-processes
    # g_logger.info("Server Started!!!")
    # tornado.ioloop.IOLoop.current().start()

    # adv multiple sub-process
    sockets = bind_sockets(8530)
    tornado.process.fork_processes(0)

    from ThinkSocks.ThinkSocks import ThinkSocks
    server = ThinkSocks()
    server.add_sockets(sockets)

    from pythinkutils.common.log import g_logger
    g_logger.info("Server Started!!!")

    IOLoop.current().start()

if __name__ == '__main__':
    main()