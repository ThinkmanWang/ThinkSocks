# -*- coding: utf-8 -*-

import sys
import os
import asyncio

import tornado.ioloop

from tornado.tcpserver import TCPServer
from tornado.iostream import StreamClosedError
from tornado import gen

from pythinkutils.aio.common.aiolog import g_aio_logger
from ThinkSocks.ThinkSocks import ThinkSocks

def main():
    server = ThinkSocks()
    server.listen(8530)
    # server.bind(8530)
    # server.start(0)  # Forks multiple sub-processes

    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()