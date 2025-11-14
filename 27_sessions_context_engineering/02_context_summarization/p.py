import asyncio
import time
import threading
from rich import print

# Synchronous approach
def make_coffee_sync():
    print(f"\tMaking coffee... : Thread Name: {threading.current_thread().name}")
    time.sleep(2)  # Simulate coffee preparation time
    print("\tCoffee is ready!")

def make_pastry_sync():
    print(f"\tMaking pastry... : Thread Name: {threading.current_thread().name}")
    time.sleep(3)  # Simulate pastry preparation time
    print("\tPastry is ready!")

def order_sync():
    make_coffee_sync()
    make_pastry_sync()


# order_sync()


async def make_coffee_aasync():
    print(f"\tMaking coffee...: thread Name: {threading.current_thread().name}")
    asyncio.sleep(3)


async def make_pastry_aasync():
    print(f"\tMaking coffee...: thread Name: {threading.current_thread().name}")
    asyncio.sleep(2)

async def  order_sync():
    pass
    
        
     
