from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
import fasttext
from tqdm import tqdm
from chainer.finders.finder import Finder

from chainer.lang.ca import normalize


class NeighborFinder(Finder):
    def __init__(self, words: set, model_path: str = "cc.ca.300.bin"):
        super().__init__("neighbors.json")
        self.words = words
        self.model = fasttext.load_model(model_path)
        self.index = defaultdict(list)

    def build_index(self):
        self.load_index()

        with ThreadPoolExecutor() as executor:
            executor.map(self.find_neighbors, tqdm(self.words))

    def find_neighbors(self, word):
        neighbors = self.model.get_nearest_neighbors(word, k=20)
        normalized_word = normalize(word)
        for neighbor in neighbors:
            neighbor_word = normalize(neighbor[1])
            if neighbor_word not in self.words:
                continue
            if normalized_word in neighbor_word:
                continue
            self.index[word].append(neighbor_word)

    def get_neighbors(self, word):
        if word not in self.index:
            self.find_neighbors(word)
        return self.index[word]
