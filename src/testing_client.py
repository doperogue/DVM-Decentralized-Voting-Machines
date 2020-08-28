import P2P
import asyncio


async def client_things():
	await P2P.port_scan()

if __name__ == '__main__':
	P2P.HELLO_MY_NAME_IS = 'client'
	asyncio.get_event_loop().run_until_complete(client_things())
	asyncio.get_event_loop().run_forever()
