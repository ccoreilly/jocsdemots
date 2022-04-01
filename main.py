from itertools import chain
from chainer import (
    WordChainer,
    AnagramFinder,
    DerivatsFinder,
    IntegratsFinder,
    NeighborFaissFinder,
    SubstitutsFinder,
)

print("Reading words")
words = set(line.strip().lower() for line in open("dict/DISC2-LP.txt"))

chainer = WordChainer()
chainer.register_finder(AnagramFinder(words)).register_finder(
    SubstitutsFinder(words)
).register_finder(DerivatsFinder(words)).register_finder(
    IntegratsFinder(words)
).register_finder(
    NeighborFaissFinder(words)
)

chainer.build_indices()
chainer.beam_width = 20
chainer.find_chain("enfonsar")
