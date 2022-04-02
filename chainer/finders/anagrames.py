from collections import defaultdict
from typing import List
from tqdm import tqdm
from chainer.finders.finder import Finder
from chainer.lang.ca import normalize, extra_chars

anagram_weights = {
    # " ": 2,
    "a": 3,
    "b": 5,
    "c": 7,
    "ç": 11,
    "d": 13,
    "e": 17,
    "f": 19,
    "g": 23,
    "h": 29,
    "i": 31,
    "j": 37,
    "k": 41,
    "l": 43,
    # "l·l": 47,
    "m": 53,
    "n": 59,
    "o": 61,
    "p": 67,
    "q": 71,
    "r": 73,
    "s": 79,
    "t": 83,
    "u": 89,
    "v": 97,
    "w": 101,
    "x": 103,
    "y": 107,
    "z": 109,
}


class AnagramFinder(Finder):
    def __init__(self, words: set):
        super().__init__(".motcache/anagrames.json")
        self.words = words
        self.index = defaultdict(set)

    def build_index(self, force: bool = False):
        if not force and self.load_index():
            return

        for word in tqdm(self.words):
            anagramproduct = self.calculate_product(word)
            if anagramproduct > 1:
                self.index[anagramproduct].add(word)
        self.dump()

    def calculate_product(self, word: str) -> int:
        normalized_word = normalize(word)
        for extra_char in extra_chars:
            normalized_word = normalized_word.replace(extra_char, "")
        anagramproduct = 1
        for letter in normalized_word:
            anagramproduct = anagramproduct * anagram_weights[letter]
        return anagramproduct

    def find_words(self, word: str) -> List[str]:
        anagramproduct = str(self.calculate_product(word))
        if anagramproduct in self.index:
            return list(key for key in self.index[anagramproduct] if key != word)
        return []
