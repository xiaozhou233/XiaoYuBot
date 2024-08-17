import tornado.ioloop
import tornado.websocket
import tornado.gen
import PluginManager
import json


class WSClient:
    def __init__(self, url):
        self.url = url
        print(f"Initializing client for {self.url}")

    @tornado.gen.coroutine
    def connect(self):
        try:
            self.connection = yield tornado.websocket.websocket_connect(self.url)
            print(f"Connected to {self.url}")
            self.listen()
        except Exception as e:
            print(f"Failed to connect: {e}")
            tornado.ioloop.IOLoop.current().stop()
            # Reconnect after 5 seconds
            tornado.ioloop.IOLoop.current().call_later(5, self.connect)
            return
        

    @tornado.gen.coroutine
    def listen(self):
        while True:
            try:
                message = yield self.connection.read_message()
                if message is None:
                    print("Connection closed")
                    break
                print(f"Received message: {message}")
                
                revMsg = json.loads(message)
                if revMsg.get("group_id") in [650559268, 767166970]:
                    for plugin in plugins:
                        plugin.on_message(revMsg)

            except Exception as e:
                print(f"Error reading message: {e}")
                
        tornado.ioloop.IOLoop.current().stop()

    def send_message(self, message):
        if self.connection:
            self.connection.write_message(message)

def main():
    url = "ws://8.137.121.212:64693"
    client = WSClient(url)
    tornado.ioloop.IOLoop.current().spawn_callback(client.connect)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    try:
        pm = PluginManager.PluginManager("plugins")
        pm.load_plugins()
        plugins = pm.get_plugins()
        main()
    except KeyboardInterrupt:
        print("Exiting...")
        tornado.ioloop.IOLoop.current().stop()
        exit(0)
    except Exception as e:
        print(f"Error: {e}")
