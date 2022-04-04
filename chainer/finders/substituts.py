from collections import defaultdict
from typing import List
from tqdm import tqdm
from chainer.finders.finder import Finder
from chainer.finders.masked_indexer import MaskedIndexer
from chainer.lang.ca import normalize


class SubstitutsFinder(Finder):
    def __init__(self, words: set):
        super().__init__("substituts.json")
        self.words = words
        self.index = defaultdict(list)
        self.indexer = MaskedIndexer(words)

    def build_index(self, force: bool = False):
        self.indexer.build_index(force)
        self.index = self.indexer.index

    def mask(self, word: str, index: int):
        return word[:index] + "*" + word[index + 1 :]

    def masked(self, word: str):
        for index in range(len(word)):
            yield self.mask(word, index)

    def find_words(self, word: str) -> List[str]:
        ret = set()
        for masked_word in self.masked(word):
            if masked_word in self.index:
                ret = ret.union(self.index[masked_word])
        if len(ret) == 0:
            return []
        return list(key for key in ret if normalize(key) != normalize(word))
