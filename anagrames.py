from collections import defaultdict
from tqdm import tqdm
from finder import Finder

vocab = {
    " ": 2,
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
    "l·l": 47,
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
    "-": 113,
}


class AnagramFinder(Finder):
    def __init__(self, words: set):
        super().__init__("anagrames.json")
        self.words = words
        self.index = defaultdict(set)

    def build_index(self, force=False):
        if not force and self.load_index():
            return

        for word in tqdm(self.words):
            word = word.strip().lower()
            anagramproduct = self.calculate_product(word)
            if anagramproduct > 1:
                self.index[anagramproduct].add(word)

    def calculate_product(self, word):
        anagramproduct = 1
        position = 0
        while position < len(word):
            letter = word[position]
            if letter not in vocab:
                break
            if letter == "l" and len(word) > position + 2 and word[position + 1] == "·":
                letter = "l·l"
                position = position + 2
            anagramproduct = anagramproduct * vocab[letter]
            position += 1
        return anagramproduct

    def get_anagram(self, word: str):
        anagramproduct = str(self.calculate_product(word))
        if anagramproduct in self.index:
            return list(key for key in self.index[anagramproduct] if key != word)
