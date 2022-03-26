from collections import defaultdict
import json
import faiss
from tqdm import tqdm
import numpy as np
from finder import Finder

from utils import normalize, set_default


class NeighborFaissFinder(Finder):
    def __init__(self, words: set, vector_filepath: str = "pruned.vec"):
        super().__init__("neighbors_faiss.index")
        self.words = words
        self.vector_filepath = vector_filepath
        self.index = faiss.IndexFlatL2(300)
        self.vector_array = []
        self.vector_map = defaultdict(int)

    def build_index(self):
        with open(self.vector_filepath) as vector_file:
            for line in tqdm(vector_file):
                if line == "2000000 300":
                    continue
                fasttext_data = line.split()
                fasttext_word = fasttext_data[0]
                if normalize(fasttext_word) not in self.words:
                    continue
                self.build_vector_map(fasttext_data)
        self.index.add(
            np.array([elem[1] for elem in self.vector_array], dtype=np.float32)
        )

    def build_vector_map(self, data):
        vector_data = [
            data[0],
            [float(elem) for elem in data[1:]],
        ]
        self.vector_array.append(vector_data)
        self.vector_map[data[0]] = len(self.vector_array) - 1

    def get_neighbors(self, word):
        ret = []
        if word not in self.vector_map:
            return ret
        vector = self.vector_array[self.vector_map[word]][1]
        D, I = self.index.search(np.array([vector], dtype=np.float32), 20)
        for neighbor_index in I[0]:
            neighbor = self.vector_array[neighbor_index][0]
            normalized_neighbor = normalize(neighbor)
            normalized_word = normalize(word)
            if (
                normalized_word in normalized_neighbor
                or normalized_neighbor in normalized_word
            ):
                continue
            ret.append(normalized_neighbor)
        return ret

    def dump(self):
        raise "Not implemented"
