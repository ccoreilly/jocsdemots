from pathlib import Path
from chainer import (
    WordChainer,
    AnagramFinder,
    DerivatsFinder,
    IntegratsFinder,
    NeighborFaissFinder,
    SubstitutsFinder,
)
from chainer.lang.ca import validate
from chainer.utils import prune_fasttext_vectors

print("Reading words")
words = set()
if Path.is_file(Path("tiralmot-sc-valid.txt")):
    words = set(line.strip() for line in open("tiralmot-sc-valid.txt"))
else:
    with open("tiralmot-sc.txt") as all_words:
        with open("tiralmot-sc-valid.txt", "w") as valid_words:
            for line in all_words:
                if (
                    validate(line)
                    and not line.strip().isupper()
                    and not line.strip().lower().endswith("ment")
                ):
                    valid_words.write(line)
                    words.add(line.strip())

if not Path.is_file(Path("tiralmot-fasttext-pruned.vec")):
    print("Pruning fasttext vectors")
    prune_fasttext_vectors("cc.ca.300.vec", "tiralmot-fasttext-pruned.vec", words)

chainer = WordChainer()
chainer.register_finder(AnagramFinder(words)).register_finder(
    SubstitutsFinder(words)
).register_finder(DerivatsFinder(words)).register_finder(
    IntegratsFinder(words)
).register_finder(
    NeighborFaissFinder(words, vector_filepath="tiralmot-fasttext-pruned.vec")
)

chainer.build_indices()
chainer.beam_width = 30
# wordtuple = tuple(words)
chainer.find_chain("dilluns", length=20)
