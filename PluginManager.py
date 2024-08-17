import os
import importlib.util
import inspect

class PluginManager:
    def __init__(self, plugin_dir):
        self.plugin_dir = plugin_dir
        self.plugins = []

    def load_plugins(self):
        for filename in os.listdir(self.plugin_dir):
            if filename.endswith(".py"):
                module_name = filename[:-3]  
                file_path = os.path.join(self.plugin_dir, filename)
                
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)

                # 查找 Plugin 类
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if name == "Plugin":
                        self.register_plugin(obj())

    def register_plugin(self, plugin):
        self.plugins.append(plugin)

    def unregister_plugin(self, plugin):
        if plugin in self.plugins:
            self.plugins.remove(plugin)
        else:
            print(f"Plugin {plugin} not found in the list of loaded plugins.")

    def get_plugins(self):
        return self.plugins
    