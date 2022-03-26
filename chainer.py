from random import randrange, shuffle

from numpy import sort
from utils import levenshtein, normalize
from anagrames import AnagramFinder
from derivats import DerivatsFinder
from integrats import IntegratsFinder
from neighbors import NeighborFinder
from neighbors_faiss import NeighborFaissFinder
from substituts import SubstitutsFinder

print("Reading words")
words = set(line.strip().lower() for line in open("dict/DISC2-LP.txt"))

print("Building anagram index")
anagrams = AnagramFinder(words)
anagrams.build_index()
# anagrams.dump()

print("Building substitutes index")
substituts = SubstitutsFinder(words)
substituts.build_index()
# substituts.dump()

print("Building derivats index")
derivats = DerivatsFinder(words)
derivats.build_index()
# derivats.dump()

print("Building integrats index")
integrats = IntegratsFinder(words)
integrats.build_index()
# integrats.dump()

print("Building semantic neighbor index")
neighbors = NeighborFaissFinder(words)
neighbors.build_index()
# neighbors.dump()


def get_words(jump_type: int, word: str):
    if jump_type == 1:
        return anagrams.get_anagram(word)
    elif jump_type == 2:
        return substituts.near_words(word)
    elif jump_type == 3:
        return derivats.near_words(word)
    elif jump_type == 4:
        return integrats.near_words(word)
    elif jump_type == 5:
        return neighbors.get_neighbors(word)
    return []


def sort_by_levenshtein(seed, words):
    def get_distance(elem):
        return elem[0]

    to_sort = []
    for word in words:
        distance = levenshtein(seed, word)
        to_sort.append((distance, word))
    to_sort.sort(key=get_distance, reverse=True)
    return [elem[1] for elem in to_sort]


while True:
    word = input("Paraula: ")
    word = normalize(word)
    chain = [{"word": word, "type": 0}]
    chain_types = []
    limit = 2000
    while len(chain) < 25 and limit > 0:
        jump_type = randrange(1, 6)
        if (
            len([chain_type for chain_type in chain_types if chain_types == jump_type])
            > 7
        ):
            continue

        if len(chain_types) > 1 and chain_types[-1] == jump_type == chain_types[-2]:
            continue
        chain_word = chain[-1]
        possible_words = get_words(jump_type, chain_word)
        if not possible_words or len(possible_words) == 0:
            limit -= 1
            continue
        if jump_type == 5:
            possible_words = sort_by_levenshtein(chain_word, possible_words)
        else:
            if len(chain) > 1:
                possible_words = sort_by_levenshtein(chain[-2], possible_words)
            else:
                shuffle(possible_words)
        for candidate in possible_words:
            if candidate not in chain and candidate[:3] not in chain_word:
                chain.append({"word": candidate, "type": jump_type})
                chain_types.append(jump_type)
                break
    print(chain)
