import asyncio

async def delete(msg, time):
    try:
        await asyncio.sleep(time)
        await msg.delete()
    except Exception as e:
        pass
    