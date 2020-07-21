# -*- coding: UTF-8 -*-

import sys
import os

import asyncio
import random

from pythinkutils.aio.redis.BaseAioRedisTaskQueue import BaseAioRedisTaskQueue
from pythinkutils.common.log import g_logger
from pythinkutils.common.datetime_utils import *

class MyAioTaskQueue(BaseAioRedisTaskQueue):

    async def on_task(self, szMsg):
        # await asyncio.sleep(5)
        # random.randint
        g_logger.debug(szMsg)
        await asyncio.sleep(random.randint(3, 6))


async def producer():
    while True:
        await asyncio.sleep(random.randint(1, 5))
        BaseAioRedisTaskQueue.put_nowait("task_queue_default", get_current_time_str())

def main():
    loop = asyncio.get_event_loop()

    taskQueue = MyAioTaskQueue(queueName="task_queue_default", size=8)
    taskQueue.start()
    asyncio.gather(producer())

    loop.run_forever()

if __name__ == '__main__':
    main()