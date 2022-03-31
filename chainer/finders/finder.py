import json
from pathlib import Path
from typing import List

from chainer.utils import set_default


class Finder:
    def __init__(self, index_file: str = "finder.json"):
        self.index_file = index_file

    def build_index(self):
        raise Exception("Not implemented")

    def load_index(self):
        if Path.is_file(Path(self.index_file)):
            with open(self.index_file) as file:
                self.index = json.load(file)
            return True

    def dump(self):
        with open(self.index_file, "w") as file:
            json.dump(self.index, file, default=set_default, indent=4)

    def find_words(self, word: str) -> List[str]:
        raise Exception("Not implemented")
