from collections import defaultdict
from tqdm import tqdm


class SubstitutsFinder:
    def __init__(self, words: set):
        self.words = words
        self.index = defaultdict(list)

    def build_index(self):
        for word in tqdm(self.words):
            for w in self.wildcarded(word):
                self.index[w].append(word)

    def wildcard(self, s, idx):
        return s[:idx] + "?" + s[idx + 1 :]

    def wildcarded(self, s):
        for idx in range(len(s)):
            yield self.wildcard(s, idx)

    def near_words(self, word):
        ret = []
        for w in self.wildcarded(word):
            ret += self.index[w]
        return [key for key in ret if key != word]
