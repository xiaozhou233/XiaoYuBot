import tornado.ioloop
from utils.WebsocketClient import WebSocketClient
import utils.Config as Config

async def main():
    try:
        # 读取配置文件
        ConfigHandle = Config.FileConfig("config.json")
        bot_config = ConfigHandle.read_config()
        
        # 连接WebSocket服务器
        ws_client = WebSocketClient(bot_config.get("ws_url"))
        
        # 加载并注册插件
        await ws_client.plugin_manager.load_plugins()
        
        await ws_client.start()
        ws = ws_client.get_connection()
    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    try:
        tornado.ioloop.IOLoop.current().run_sync(main)
    except KeyboardInterrupt:
        print("[INFO] 程序已终止")
