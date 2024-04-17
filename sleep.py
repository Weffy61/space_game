import asyncio


async def async_sleep(time):
    for i in range(time):
        await asyncio.sleep(0)
