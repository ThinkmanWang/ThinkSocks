# -*- coding: utf-8 -*-

import aiohttp
import asyncio

async def main():
    async with aiohttp.ClientSession() as session:
        dictData = {
            "userId": 11230
            , "secretKey": "c3c9e7abd5cc47c7050a89f5a4372b89"
            , "activityId": 13
            , "startTime": "2020-07-20 00:00:00"
            , "endTime": "2020-07-20 23:59:59"
            , "pageNo": 1
            , "pageSize": 10
        }
        resp = await session.post("https://distributeconsole.jiegames.com/api/getDataDetail", data=dictData)
        print(await resp.text())



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
