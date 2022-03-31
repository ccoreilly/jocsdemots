import json
from pathlib import Path

from utils import set_default


class Finder:
    def __init__(self, index_file="finder.json"):
        self.index_file = index_file

    def load_index(self):
        if Path.is_file(Path(self.index_file)):
            with open(self.index_file) as file:
                self.index = json.load(file)
            return True

    def dump(self):
        with open(self.index_file, "w") as file:
            json.dump(self.index, file, default=set_default, indent=4)
