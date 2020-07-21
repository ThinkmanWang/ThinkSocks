# -*- coding: UTF-8 -*-

import sys
import os

import asyncio
from pythinkutils.aio.kafka.ThinkAioKafkaConsumer import ThinkAioKafkaConsumer
from pythinkutils.config.Config import g_config
from pythinkutils.aio.common.aiolog import g_aio_logger

from pythinkutils.aio.kafka.ThinkAioKafkaProducer import ThinkAioKafkaProducer
from pythinkutils.common.datetime_utils import *

class TestConsumer(ThinkAioKafkaConsumer):

    def __init__(self, szHost, szTopic, szGroup):
        super().__init__(szHost, szTopic, szGroup)

    async def on_msg(self, msg):
        # await asyncio.sleep(5)
        # random.randint
        # print("consumed: ", msg.topic, msg.partition, msg.offset, msg.key, msg.value, msg.timestamp)
        szMsg = str(msg.value, "utf-8")
        await g_aio_logger.info(szMsg)

async def send_test():
    while True:
        await asyncio.sleep(5)
        nRet = await ThinkAioKafkaProducer.send(g_config.get("kafka", "host"), g_config.get("kafka", "topic"), get_current_time_str())
        await g_aio_logger.info(nRet)

def main():
    loop = asyncio.get_event_loop()

    myConsumer = TestConsumer(g_config.get("kafka", "host"), g_config.get("kafka", "topic"), "thinkman")
    myConsumer.start()

    asyncio.gather(send_test())

    loop.run_forever()

if __name__ == '__main__':
    main()
