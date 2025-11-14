import asyncio

async def task_a():
    for i in range(5):
        print("A working:", i)


asyncio.run(task_a())   