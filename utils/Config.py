import json

class FileConfig:
    def __init__(self, file_path):
        self.file_path = file_path
        self._config = None

    def read_config(self):
        try:
            with open(self.file_path, 'r') as f:
                self._config = json.load(f)
        except FileNotFoundError:
            print(f"Error: The file {self.file_path} was not found.")
            self._config = {}
        except json.JSONDecodeError:
            print(f"Error: The file {self.file_path} contains invalid JSON.")
            self._config = {}
        return self._config
    
    @property
    def config(self):
        if self._config is None:
            self.read_config()
        return self._config
    