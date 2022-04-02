from collections import defaultdict
from typing import List
from tqdm import tqdm
from chainer.finders.finder import Finder
from chainer.finders.masked_indexer import MaskedIndexer

vocab = [
    "a",
    "b",
    "c",
    "ç",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "l·l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
]


class IntegratsFinder(Finder):
    def __init__(self, words: set):
        super().__init__(".motcache/integrats.json")
        self.words = words
        self.index = defaultdict(list)
        self.indexer = MaskedIndexer(words)

    def build_index(self, force: bool = False):
        self.indexer.build_index(force)
        self.index = self.indexer.index

    def add_mask(self, word: str):
        for index in range(len(word) + 1):
            yield word[:index] + "*" + word[index:]

    def find_words(self, word: str) -> List[str]:
        ret = set()
        for masked_word in self.add_mask(word):
            if masked_word in self.index:
                ret = ret.union(self.index[masked_word])
        if len(ret) == 0:
            return []
        return list(key for key in ret if key != word)
