from collections import defaultdict
import fasttext
from tqdm import tqdm


class NeighborFinder:
    def __init__(self, words: set, model_path: str = "cc.ca.300.bin"):
        self.words = words
        self.model = fasttext.load_model(model_path)
        self.index = defaultdict(list)

    def build_index(self):
        for word in tqdm(self.words):
            neighbors = self.model.get_nearest_neighbors(word, k=20)
            for neighbor in neighbors:
                if neighbor not in self.words:
                    continue
                if word in neighbor:
                    continue
                self.index[word].append(neighbor)

    def get_neighbors(self, word):
        if word not in self.index:
            return []
        return self.index[word]
