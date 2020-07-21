# -*- coding: UTF-8 -*-

import sys
import os

import asyncio
import datetime
import logging
import os
import time
from logging import LogRecord
from tempfile import NamedTemporaryFile
from aiofiles.threadpool import AsyncTextIOWrapper
from aiologger import Logger

from aiologger.handlers.files import (
    AsyncFileHandler,
    BaseAsyncRotatingFileHandler,
    AsyncTimedRotatingFileHandler,
    RolloverInterval,
    ONE_WEEK_IN_SECONDS,
    ONE_DAY_IN_SECONDS,
    ONE_MINUTE_IN_SECONDS,
    ONE_HOUR_IN_SECONDS,
)
from aiologger.handlers.files import AsyncStreamHandler

from pythinkutils.common.FileUtils import *

def setup_custom_logger():
    LOG_PATH = 'log'
    FileUtils.create_folder_if_not_exists(LOG_PATH)

    handler = AsyncTimedRotatingFileHandler(
        filename="log/think.log",
        when=RolloverInterval.HOURS,
        backup_count=48,
    )
    formatter = logging.Formatter("[%(asctime)s] %(threadName)s - %(pathname)s %(funcName)s():%(lineno)d  %(levelname)s %(message)s")
    handler.formatter = formatter

    logger = Logger.with_default_handlers(formatter=formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    return logger

g_aio_logger = setup_custom_logger()

# async def main():
#     await g_aio_logger.debug("FXXK")
#
# if __name__ == '__main__':
#     asyncio.run(main())
