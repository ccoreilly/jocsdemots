from collections import defaultdict
from tqdm import tqdm
from finder import Finder


class SubstitutsFinder(Finder):
    def __init__(self, words: set):
        super().__init__("substituts.json")
        self.words = words
        self.index = defaultdict(list)

    def build_index(self):
        if self.load_index():
            return
        for word in tqdm(self.words):
            for w in self.wildcarded(word):
                self.index[w].append(word)

    def wildcard(self, s, idx):
        return s[:idx] + "?" + s[idx + 1 :]

    def wildcarded(self, s):
        for idx in range(len(s)):
            yield self.wildcard(s, idx)

    def near_words(self, word):
        ret = set()
        for w in self.wildcarded(word):
            if w in self.index:
                ret = ret.union(self.index[w])
        if len(ret) == 0:
            return None
        return list(key for key in ret if key != word)
