from collections import defaultdict
from typing import List
from tqdm import tqdm
from chainer.finders.finder import Finder


class DerivatsFinder(Finder):
    def __init__(self, words: set):
        super().__init__(".motcache/derivats.json")
        self.words = words
        self.index = defaultdict(list)

    def build_index(self):
        if self.load_index():
            return
        for word in tqdm(self.words):
            for shorted_word in self.less_letters(word):
                if shorted_word in self.words:
                    self.index[word].append(shorted_word)
        self.dump()

    def remove_letter(self, word: str, index: int):
        return word[:index] + word[index + 1 :]

    def less_letters(self, word: str):
        for index in range(len(word)):
            yield self.remove_letter(word, index)

    def find_words(self, word: str) -> List[str]:
        if word in self.index:
            return self.index[word]
        return []
