from collections import defaultdict
from tqdm import tqdm

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


class AnagramFinder:
    def __init__(self, words: set):
        self.words = words
        self.index = defaultdict(list)
        self.word2index = {}

    def build_index(self):
        # temp_index = defaultdict(list)
        for word in tqdm(self.words):
            anagramproduct = 1
            word = word.strip().lower()
            position = 0
            while position < len(word):
                letter = word[position]
                if letter not in vocab:
                    break
                if (
                    letter == "l"
                    and len(word) > position + 2
                    and word[position + 1] == "·"
                ):
                    letter = "l·l"
                    position = position + 2
                anagramproduct = anagramproduct * vocab[letter]
                position += 1
            if anagramproduct > 1:
                self.word2index[word] = anagramproduct
                self.index[anagramproduct].append(word)
        # self.index = {key:value for key, value in temp_index.items() if len(value) > 1}

    def get_anagram(self, word: str):
        if word not in self.word2index:
            return []
        return [key for key in self.index[self.word2index[word]] if key != word]
