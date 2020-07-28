# -*- coding: utf-8 -*-

import asyncio
from pythinkutils.aio.watchdog.AIOWatchdog import AIOWatchdog, AIOEventHandler

WATCH_DIR = "/Users/wangxiaofeng/Github-Thinkman/ThinkSocks"

class MyEventHandler(AIOEventHandler):
    """Subclass of asyncio-compatible event handler."""
    async def on_created(self, event):
        print('Created:', event.src_path)  # add your functionality here

    async def on_deleted(self, event):
        print('Deleted:', event.src_path)  # add your functionality here

    async def on_moved(self, event):
        print('Moved:', event.src_path)  # add your functionality here

    async def on_modified(self, event):
        print('Modified:', event.src_path)  # add your functionality here


async def watch_fs(watch_dir):
    evh = MyEventHandler()
    watch = AIOWatchdog(watch_dir, event_handler=evh)
    watch.start()
    for _ in range(60):
        await asyncio.sleep(1)
    watch.stop()


asyncio.get_event_loop().run_until_complete(watch_fs(WATCH_DIR))