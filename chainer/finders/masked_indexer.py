from collections import defaultdict
import json
from pathlib import Path
from tqdm import tqdm
from chainer.lang.ca import normalize, extra_chars
from chainer.utils import set_default


class MaskedIndexer:
    def __init__(self, words: set, index_file: str = ".motcache/masked_words.json"):
        self.words = words
        self.index = defaultdict(list)
        self.index_file = index_file

    def build_index(self, force: bool = False):
        if not force and self.load_index():
            return
        for word in tqdm(self.words):
            normalized_word = normalize(word).replace("l·l", "Ŀ")
            for extra_char in extra_chars:
                normalized_word = normalized_word.replace(extra_char, "")
            for masked_word in self.masked(normalized_word):
                self.index[masked_word].append(word)
        self.dump()

    def mask(self, word: str, index: int):
        return word[:index] + "*" + word[index + 1 :]

    def masked(self, word: str):
        for index in range(len(word)):
            yield self.mask(word, index)

    def load_index(self):
        if not Path.is_file(Path(self.index_file)):
            return False

        with open(self.index_file) as file:
            self.index = json.load(file)
        return True

    def dump(self):
        with open(self.index_file, "w") as file:
            json.dump(self.index, file, default=set_default, indent=4)
