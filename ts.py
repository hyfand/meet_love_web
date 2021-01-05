import asyncio
async def fun():
    print("fku")


loop = asyncio.get_event_loop()
loop.run_until_complete(fun())
# py3.7 以后
# asyncio.run()