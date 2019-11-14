from aiohttp import ClientSession, TCPConnector
import asyncio


# class Client:
# def __init__(self):
#     self._cs = ClientSession()

async def get(url):
    async with ClientSession() as cs:
        async with cs.get(url) as resp:
            return url, await resp.text()

    # async def close(self):
    #     await self._cs.close()


async def func():
    # client = Client()
    urls = [
        "http://youku.com",
        "http://baidu.com",
        "http://163.com",
        "http://sui.com",
        "http://baidu.com",
        "http://163.com",
        "http://sui.com",
        "http://51.com",
    ]
    for i in urls:
        print(await get(i))
    # await client.close()


async def sample():
    async with ClientSession as session:
        async with session.get('http://httpbin.org/get') as resp:
            print(resp.status)
            print(await resp.text())


# -----------------

tasks = []
url = "https://www.baidu.com/{}"


async def hello(url):
    async with ClientSession() as session:
        async with session.get(url) as response:
            response = await response.read()
            print(response)


#
if __name__ == "__main__":
    asyncio.run(hello(url))
