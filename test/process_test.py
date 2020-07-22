# -*- coding: utf-8 -*-

import sys
import os
import asyncio

import tornado.ioloop
import tornado
import tornado.process

from tornado.tcpserver import TCPServer

def main():
    # server = ThinkSocks()
    # server.listen(8530)
    # g_logger.info("Server Started!!!")
    # tornado.ioloop.IOLoop.instance().start()

    # multiple sub-process
    server = TCPServer()
    server.bind(8530)
    server.start(0)  # Forks multiple sub-processes
    print("FXXK")
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()