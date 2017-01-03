import asyncio
import aiohttp
import async_timeout

async def http(context):
    await asyncio.sleep(context.frequency)
    async with aiohttp.ClientSession(loop=context.loop) as session:

        try:
            with async_timeout.timeout(context.timeout):
                async with session.get(context.extra['uri']) as response:
                    context.handler(response, context)

        except asyncio.TimeoutError:
            context.new_incident('timeout')
            context.house_keeping()
