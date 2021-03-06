# -*- coding: utf-8 -*-

import asyncio
import aiofiles

async def main():
    async with aiofiles.open("/Users/wangxiaofeng/Github-Thinkman/ThinkSocks/README.md", mode="r") as f:
        async for szLine in f:
            print(szLine)

    async with aiofiles.open("/Users/wangxiaofeng/Github-Thinkman/ThinkSocks/README.md", mode="r") as f:
        contents = await f.read()
        print(contents)

if __name__ == '__main__':
    asyncio.run(main())