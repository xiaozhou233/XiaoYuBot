import json
import tornado.websocket
from utils.Plugin import PluginManager

class WebSocketClient:
    def __init__(self, url):
        self.url = url
        self.ws = None
        self.plugin_manager = PluginManager()

    async def connect(self):
        self.ws = await tornado.websocket.websocket_connect(self.url)
        print("WebSocket connected")
        await self.listen()

    async def listen(self):
        while True:
            msg = await self.ws.read_message()
            if msg is None:
                break
            msg = json.loads(msg)
            await self.plugin_manager.handle_message(msg, self)

    async def send_message(self, message):
        if self.ws:
            await self.ws.write_message(message)
        else:
            print("WebSocket is not connected.")

    async def call_onebot_api(self, api, data):
        await self.send_message(json.dumps({"action": api, "params": data, "echo":"sent"}))
    
    async def send_group_msg(self, group_id, message):
        await self.call_onebot_api("send_group_msg", {"group_id": group_id, "message": message})

    def get_connection(self):
        return self.ws

    async def start(self):
        await self.connect()

    def register_plugin(self, plugin):
        self.plugin_manager.register_plugin(plugin)
