import os
import importlib

class Plugin:
    def __init__(self, config=None):
        self.config = config

    async def on_message(self, message, ws_client):
        raise NotImplementedError("Plugins must implement this method.")


class PluginManager:
    def __init__(self):
        self.plugins = []

    def register_plugin(self, plugin):
        if isinstance(plugin, Plugin):
            self.plugins.append(plugin)
        else:
            raise ValueError("Invalid plugin type")

    async def handle_message(self, message, ws_client):
        for plugin in self.plugins:
            await plugin.on_message(message, ws_client)

    async def load_plugins(self, plugin_folder='plugins'):
        for filename in os.listdir(plugin_folder):
            if filename.endswith('.py') and not filename.startswith('__'):
                module_name = filename[:-3]
                module = importlib.import_module(f'{plugin_folder}.{module_name}')
                for attr in dir(module):
                    plugin_class = getattr(module, attr)
                    if isinstance(plugin_class, type) and issubclass(plugin_class, Plugin) and plugin_class is not Plugin:
                        plugin_instance = plugin_class()
                        self.register_plugin(plugin_instance)
