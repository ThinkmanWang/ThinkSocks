# -*- coding: UTF-8 -*-

import sys
import os
import asyncio

from abc import *
from aiokafka import AIOKafkaConsumer
from pythinkutils.aio.common.aiolog import g_aio_logger
from pythinkutils.config.Config import g_config

class ThinkAioKafkaConsumer(object):
    __metaclass__ = ABCMeta

    def __init__(self, szHost, szTopic, szGroup):
        self.m_szHost = szHost
        self.m_szTopic = szTopic
        self.m_szGroup = szGroup
        self.m_bStarted = False

    def start(self):
        if self.m_bStarted:
            return

        asyncio.gather(self.on_start())

        self.m_bStarted = True

    @abstractmethod
    async def on_msg(self, msg):
        pass

    async def on_start(self):
        while True:
            consumer = AIOKafkaConsumer(self.m_szTopic, loop=asyncio.get_event_loop(), bootstrap_servers=self.m_szHost, group_id=self.m_szGroup)

            try:
                await consumer.start()

                # Consume messages
                async for msg in consumer:
                    await self.on_msg(msg)
                    # print("consumed: ", msg.topic, msg.partition, msg.offset, msg.key, msg.value, msg.timestamp)
            except Exception as e:
                pass
                # await g_aio_logger.error(e)
            finally:
                consumer.stop()

