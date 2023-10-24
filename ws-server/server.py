import websockets as wbs
from websockets.server import serve
import asyncio
import json
import http
import sys
import datetime as dt

def timestamp():
    return dt.datetime.now().strftime("%H:%M:%S")

class Server:
    def __init__(self, is_local: bool, port=6969):
        if is_local: self.local_name = "localhost"
        else: self.local_name = ""
        self.port = port
        self.users = {}
        self.admin = None
        self.usersMsgs = {}
        self.data = json.load(open("ws-server/data.bubuh", 'r'))
        self.ops = {
            "sr.song.add": {"fields": ["vid_id", "by"]},
            "sr.song.remove":{"fields":["vid_id"]},
            "serv.answer": {"fields": ["op", "status", "info", "code"]},
            "serv.ping": {"fields": []},
            "serv.check_ver": {"fields": []},
            "serv.check_ver_answer":{"fields":["ver"]},
            "serv.User_disconnect":{"fields":[]} 
        }

    async def send_error(self, ws, error, code):
        await ws.send(json.dumps({"status": "err", "info": error, "code": str(code)}))

    async def check_and_return_json(self, ws, data):
        try: dataNew = json.loads(data)
        except json.JSONDecodeError:
            await self.send_error(ws, "data in isnt json format", 6901)
            return None
        if type(dataNew) != type(dict()):
            await self.send_error(ws, "data in isnt json format", 6901)
            return None
        return dataNew
        
    async def need_fields(self, ws, data, *args, **kwargs):
        if "list" in kwargs.keys():
            for i in kwargs['list']:
                if not i in data.keys():
                    await self.send_error(ws, "data dont have needed fields", 6902)
                    return False
            return True
        else:
            for i in args:
                if not i in data.keys():
                    await self.send_error(ws, "data dont have needed fields", 6902)
                    return False
            return True

    async def newUser(self, ws):
        await ws.send(json.dumps({"status": "ok", "info": "connected, please send your identificator", "code": "6900"}))
        id_ = None
        async with asyncio.timeout(30):
            id_ = await self.check_and_return_json(ws, await ws.recv())
        if id_:
            if await self.need_fields(ws, id_, "nick", "pass", "data"):
                if id_['nick'] == "ppSpin":
                    if await self.need_fields(ws, id_['data'], "secret1", "secret2", "secret3"):
                        if id_['data']['secret1'] == self.data['admin']['secret1'] and id_['data']['secret2'] == self.data['admin']['secret2'] and id_['data']['secret3'] == self.data['admin']['secret3']:
                            await ws.send(json.dumps({
                                "status": "ok",
                                "info": "successfully authorized",
                                "code": "6900"
                            }))
                            self.admin = ws
                            try:
                                async for msg in ws:
                                    msg_data = await self.check_and_return_json(ws, msg)
                                    if msg_data:
                                        if await self.need_fields(ws, msg_data, "op", "User_nick", "data"):
                                            if msg_data['op'] in self.ops.keys():
                                                if await self.need_fields(ws, msg_data['data'], list=self.ops[msg_data['op']]['fields']):
                                                    if msg_data["User_nick"] in self.users:
                                                        self.usersMsgs[msg_data['User_nick']]['<'].append({
                                                            "by": "user",
                                                            "nick": msg_data['User_nick'],
                                                            "time": timestamp(),
                                                            "data": msg_data
                                                        })
                                                        await self.users[msg_data['User_nick']].send(json.dumps(msg_data))
                                                    else:
                                                        await self.send_error(ws, "that User is not connected", 6906)
                                            else:
                                                await self.send_error(ws, "unknown operation", 6908)
                            finally:
                                self.admin = None
                        else:
                            await self.send_error(ws, "secrets do not match", 6903)
                            return                            
                    else: return
                else:
                    if id_['nick'] in self.data['users'].keys():
                        if id_['pass'] == self.data['users'][id_['nick']]:
                            await ws.send(json.dumps({
                                "status": "ok",
                                "info": "successfully authorized",
                                "code": "6900"
                            }))
                            self.users[id_['nick']] = ws
                            self.usersMsgs[id_['nick']] = {">": [], "<": []} # > - из человека, < - в человека
                            try:
                                async for msg in ws:
                                    msg_data = await self.check_and_return_json(ws, msg)
                                    if msg_data:
                                        self.usersMsgs[id_['nick']]['>'].append({
                                            "by": "user",
                                            "nick": id_['nick'],
                                            "time": timestamp(),
                                            "data": msg_data
                                        })
                                        if await self.need_fields(ws, msg_data, "op", "data"):
                                            if msg_data['op'] in self.ops.keys():
                                                if await self.need_fields(ws, msg_data['data'], list=self.ops[msg_data['op']]['fields']):
                                                    if self.admin:
                                                        msg_data['User_nick'] = id_['nick']
                                                        await self.admin.send(json.dumps(msg_data))
                                                    else:
                                                        await self.send_error(ws, "Admin not connected", 6907)
                                            else:
                                                await self.send_error(ws, "unknown operation", 6908)
                            finally:
                                self.users.pop(id_['nick'])
                        else:
                            await self.send_error(ws, "incorrect password", 6905)
                            return
                    else:
                        await self.send_error(ws, "nick not found", 6904)
                        return
            else:
                return
        else:
            return

    async def pingpong(self, path, _):
        if path == "/pingpong":
            return http.HTTPStatus.OK, [], b"OK\n"

    async def start_ws(self):
        async with serve(self.newUser, self.local_name, self.port, process_request=self.pingpong) as ws:
            await asyncio.Future()

    def run(self): 
        asyncio.run(self.start_ws())

local = True
if len(sys.argv) > 1:
    if sys.argv[1] == "public":
        local = False

server = Server(local)
server.run()