import asyncio
async def func1():
    await asyncio.sleep(4)
    print("func-1")

async def func2():
    await asyncio.sleep(2)
    print("func-2")

async def func3():
    await asyncio.sleep(1)
    print("func-3")

async def main():
    # task =  asyncio.create_task(func1())
    # await func1()
    await asyncio.gather(func1() ,func2(),func3())
    # func2()
    # func3()
    # tasks = [] 
    # await asyncio.gather(tasks)
    
    

asyncio.run(main())