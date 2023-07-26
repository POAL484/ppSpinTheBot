import asyncio
import websockets as wbscks

async def cons_h(ws):
    async for msg in ws:
        print(msg)
        #await ws.close()

        
async def cons():
    ws_url = "wss://events.7tv.io/v3"
    async with wbscks.connect(ws_url) as ws:
        await ws.send('{"op": 35, "d": {"type": "emote_set.update", "condition": {"object_id": "6301dcecf7723932b45c06b0"}}}')
        await cons_h(ws)

loop = asyncio.get_event_loop()
loop.run_until_complete(cons())
loop.run_forever()
