from __future__ import annotations
from random import random
from typing import Dict, List, TypedDict

from numpy import sort
from chainer.utils import levenshtein
from chainer.finders import Finder


def sort_by_levenshtein(seed, words):
    def get_distance(elem):
        return elem[0]

    to_sort = []
    for word in words:
        distance = levenshtein(seed, word)
        to_sort.append((distance, word))
    to_sort.sort(key=get_distance, reverse=True)
    return [elem[1] for elem in to_sort]


class ChainNode(TypedDict):
    word: str
    chain: List[str]
    score: float
    finder_type: str
    type_weights: Dict[str, float]
    previous: ChainNode


class WordChainer:
    def __init__(self):
        self.beam_width = 5
        self.word_finders: Dict[str, Finder] = {}
        self.chain: List[ChainNode] = []

    def register_finder(self, finder: Finder):
        self.word_finders[type(finder).__name__] = finder
        return self

    def unregister_finder(self, finder: Finder):
        finder_name = type(finder).__name__
        if finder_name in self.word_finders:
            del self.word_finders[finder_name]

    def build_indices(self):
        for finder in self.word_finders.values():
            finder.build_index()

    def calculate_score(
        self, node: ChainNode, candidate: str, finder_name: str
    ) -> float:

        # if candidate in node["word"] or node["word"] in candidate:
        #     return 0

        if node["type_weights"][finder_name] == 0:
            print(f"Limit reached for {finder_name}")
            return 0
        # distance = levenshtein(node["word"], candidate)

        distance = random() * 10
        # finder_weight = 1
        # previous_finder = node["finder_type"]
        # previous_node = node["previous"]
        # while previous_node:
        #     if levenshtein(previous_node["word"], candidate) < 4:
        #         return 0
        #     if finder_name != previous_finder:
        #         finder_weight += 5
        #     previous_finder = previous_node["finder_type"]
        #     previous_node = previous_node["previous"]

        score = distance * node["type_weights"][finder_name]

        if candidate[:5] == node["word"][:5] or finder_name == node["finder_type"]:
            score = score * 0.01

        return node["score"] + score

    def initialize_word_finders_weight(self, length: int) -> Dict[str, float]:
        finder_count = len(self.word_finders)
        max_words_per_finder = length / finder_count + 1
        type_weights: Dict[str, float] = {}
        for finder_name in self.word_finders.keys():
            type_weights[finder_name] = max_words_per_finder

        # if "NeighborFaissFinder" in type_weights:
        #     type_weights["NeighborFaissFinder"] = max_words_per_finder * 3
        return type_weights

    def initialize_chain(self, seed: str, length: int):
        self.chain.append(
            {
                "word": seed,
                "chain": [seed],
                "finder_type": "initial",
                "type_weights": self.initialize_word_finders_weight(length),
                "score": 0.0,
                "previous": None,
            }
        )

    def reduce_weight(
        self, type_weights: Dict[str, float], finder_name: str
    ) -> Dict[str, float]:
        new_weights = type_weights.copy()
        if finder_name in new_weights:
            new_weights[finder_name] = max(0, new_weights[finder_name] - 1)

        return new_weights

    def find_chain(self, seed: str, length: int = 25):
        self.initialize_chain(seed, length)
        while len(self.chain) > 0 and len(self.chain[0]["chain"]) < 25:
            temp_chain: List[ChainNode] = []
            for node in self.chain:
                for finder_name, finder in self.word_finders.items():
                    candidates = finder.find_words(node["word"])
                    for candidate in candidates:
                        if candidate not in node["chain"]:
                            temp_chain.append(
                                {
                                    "word": candidate,
                                    "chain": [*node["chain"], candidate],
                                    "finder_type": finder_name,
                                    "type_weights": self.reduce_weight(
                                        node["type_weights"], finder_name
                                    ),
                                    "score": self.calculate_score(
                                        node, candidate, finder_name
                                    ),
                                    "previous": node,
                                }
                            )

            temp_chain.sort(key=lambda x: x["score"], reverse=True)
            self.chain = temp_chain[: self.beam_width]
        if len(self.chain) > 0:
            print(self.chain[0]["chain"])
            node = self.chain[0]
            print(node)
            while node:
                print(node["finder_type"])
                node = node["previous"]
        # node = self.chain[0]
        # print(node)
