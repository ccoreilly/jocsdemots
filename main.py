from re import sub
from anagrames import AnagramFinder
from neighbors import NeighborFinder
from substituts import SubstitutsFinder

print("Reading words")
words = set(line.strip().lower() for line in open("DISC2/DISC2-LP.txt"))

print("Building anagram index")
anagrams = AnagramFinder(words)
anagrams.build_index()

print("Building substitutes index")
substituts = SubstitutsFinder(words)
substituts.build_index()

print("Building semantic neighbor index")
neighbors = NeighborFinder(words)
neighbors.build_index()

while True:
    word = input("Paraula: ")
    print(anagrams.get_anagram(word))
    print(substituts.near_words(word))
