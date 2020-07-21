# -*- coding: UTF-8 -*-

import sys
import os

import sys
import os
import asyncio
import aiorwlock

from abc import *
from aiokafka import AIOKafkaProducer

from pythinkutils.aio.common.aiolog import g_aio_logger

class ThinkAioKafkaProducer(object):
    g_dictConnPool = {}
    g_rwlock = aiorwlock.RWLock()

    @classmethod
    async def send(cls, szHost, szTopic, szMsg):
        if cls.g_dictConnPool.get(szHost) is None:
            async with cls.g_rwlock.writer:
                if cls.g_dictConnPool.get(szHost) is None:
                    try:
                        producer = AIOKafkaProducer(loop=asyncio.get_event_loop(), bootstrap_servers=szHost)
                        await producer.start()

                        cls.g_dictConnPool[szHost] = producer
                    except Exception as e:
                        await g_aio_logger.error(e)

        producer = cls.g_dictConnPool.get(szHost)
        if producer is None:
            return -1

        try:
            # Produce message
            await producer.send_and_wait(szTopic, szMsg.encode("utf-8"))
            return len(szMsg)
        except Exception as e:
            del cls.g_dictConnPool[szHost]
            await producer.stop()
            return -1

