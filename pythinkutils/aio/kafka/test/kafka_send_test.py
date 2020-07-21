# -*- coding: UTF-8 -*-

import sys
import os

import asyncio
from aiokafka import AIOKafkaProducer
from pythinkutils.aio.common.aiolog import g_aio_logger
from pythinkutils.config.Config import g_config

async def send_one():
    producer = AIOKafkaProducer(loop=asyncio.get_event_loop(), bootstrap_servers=g_config.get("kafka", "host"))
    # Get cluster layout and initial topic/partition leadership information
    await producer.start()
    try:
        # Produce message
        await producer.send_and_wait(g_config.get("kafka", "topic"), b"Super message")
    except Exception as e:
        await g_aio_logger.error(e)
    finally:
        # Wait for all pending messages to be delivered or expire.
        await producer.stop()

async def main():
    await g_aio_logger.info("FXXK")
    await send_one()
    await g_aio_logger.info("DONE")


if __name__ == '__main__':
    asyncio.run(main())