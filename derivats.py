from collections import defaultdict
from tqdm import tqdm
from finder import Finder


class DerivatsFinder(Finder):
    def __init__(self, words: set):
        super().__init__("derivats.json")
        self.words = words
        self.index = defaultdict(list)

    def build_index(self):
        if self.load_index():
            return
        for word in tqdm(self.words):
            for w in self.less_letters(word):
                if w in self.words:
                    self.index[word].append(w)

    def remove_letter(self, s, idx):
        return s[:idx] + s[idx + 1 :]

    def less_letters(self, s):
        for idx in range(len(s)):
            yield self.remove_letter(s, idx)

    def near_words(self, word):
        if word in self.index:
            return self.index[word]
