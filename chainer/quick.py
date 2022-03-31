from anagrames import AnagramFinder
from derivats import DerivatsFinder
from integrats import IntegratsFinder
from neighbors import NeighborFinder
from substituts import SubstitutsFinder

print("Reading words")
words = set(line.strip().lower() for line in open("DISC2/DISC2-LP.txt"))

print("Building semantic neighbor index")
neighbors = NeighborFinder(words)
# neighbors.build_index()
# neighbors.dump()

while True:
    word = input("Paraula: ")
    print(neighbors.get_neighbors(word))
