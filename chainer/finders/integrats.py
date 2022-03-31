from collections import defaultdict
from typing import List
from tqdm import tqdm
from chainer.finders.finder import Finder

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
        super().__init__("integrats.json")
        self.words = words
        self.index = defaultdict(list)

    def build_index(self):
        if self.load_index():
            return
        for word in tqdm(self.words):
            for w in self.more_letters(word):
                if w in self.words:
                    self.index[word].append(w)

    def more_letters(self, s):
        for idx in range(len(s) + 1):
            for letter in vocab:
                yield s[:idx] + letter + s[idx:]

    def find_words(self, word: str) -> List[str]:
        if word in self.index:
            return self.index[word]
        return []
