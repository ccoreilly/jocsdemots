from utils import normalize
from anagrames import AnagramFinder
from derivats import DerivatsFinder
from integrats import IntegratsFinder
from neighbors import NeighborFinder
from neighbors_faiss import NeighborFaissFinder
from substituts import SubstitutsFinder

print("Reading words")
words = set(line.strip().lower() for line in open("DISC2/DISC2-LP.txt"))

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

while True:
    word = input("Paraula: ")
    word = normalize(word)
    print(anagrams.get_anagram(word))
    print(substituts.near_words(word))
    print(derivats.near_words(word))
    print(integrats.near_words(word))
    print(neighbors.get_neighbors(word))
