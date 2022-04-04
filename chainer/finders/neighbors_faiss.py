from collections import defaultdict
import json
from pathlib import Path
from typing import List
import faiss
from tqdm import tqdm
import numpy as np
from chainer.finders.finder import Finder
from chainer.lang.ca import normalize


class NeighborFaissFinder(Finder):
    def __init__(
        self,
        words: set[str],
        vector_filepath: str = "pruned.vec",
        normalize_words: bool = False,
    ):
        super().__init__("neighbors_faiss.index")
        self.words = words
        self.vector_filepath = vector_filepath
        self.normalize_words = normalize_words
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
                if self.normalize_words:
                    fasttext_word = normalize(fasttext_word)
                if fasttext_word not in self.words:
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

    def find_words(self, word: str) -> List[str]:
        ret = []
        if word not in self.vector_map:
            return ret
        vector = self.vector_array[self.vector_map[word]][1]
        D, I = self.index.search(np.array([vector], dtype=np.float32), 20)
        for result_index, neighbor_index in enumerate(I[0]):
            distance = D[0][result_index]
            if distance > 0.3:
                continue
            neighbor = self.vector_array[neighbor_index][0]
            # print(f"Distància entre {word} i {neighbor}: {distance}")
            if self.normalize_words:
                neighbor = normalize(neighbor)
            ret.append(neighbor)
        return ret

    def dump(self):
        raise "Not implemented"

    def load_index(self):
        if Path.is_file(Path(self.index_file)):
            with open(self.index_file) as file:
                self.index = json.load(file)
            return True
