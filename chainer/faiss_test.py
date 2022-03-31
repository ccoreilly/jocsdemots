from collections import defaultdict

from tqdm import tqdm
from utils import normalize
import faiss
import numpy as np

words = set(line.strip().lower() for line in open("dict/DISC2-LP.txt"))

print("Start indexing")

vector_array = []
vector_map = defaultdict(int)


def build_vector_map(data):
    vector_data = [
        data[0],
        [float(elem) for elem in data[1:]],
    ]
    vector_array.append(vector_data)
    vector_map[data[0]] = len(vector_array) - 1


index = faiss.IndexFlatL2(300)
# with open("cc.ca.300.vec") as vector_file:
#     with open("pruned.vec", "w") as write_file:
#         for line in tqdm(vector_file):
#             if line == "2000000 300":
#                 continue
#             fasttext_data = line.split()
#             fasttext_word = fasttext_data[0]
#             if normalize(fasttext_word) not in words:
#                 continue
#             write_file.write(line)
#             build_vector_map(fasttext_data)

with open("pruned.vec") as vector_file:
    for line in tqdm(vector_file):
        if line == "2000000 300":
            continue
        fasttext_data = line.split()
        fasttext_word = fasttext_data[0]
        if normalize(fasttext_word) not in words:
            continue
        build_vector_map(fasttext_data)


index.add(np.array([elem[1] for elem in vector_array], dtype=np.float32))
print("Index done")
print(index.ntotal)

while True:
    word = input("Paraula: ")
    try:
        if word not in vector_map:
            print("Paraula no trobada")
            continue
        vector = vector_array[vector_map[word]][1]
        D, I = index.search(np.array([vector], dtype=np.float32), 20)
        print(D)
        print(I)
        for trobat in I[0]:
            neighbor = vector_array[trobat][0]
            normalized_neighbor = normalize(neighbor)
            normalized_word = normalize(word)
            # if (
            #     normalized_word in normalized_neighbor
            #     or normalized_neighbor in normalized_word
            # ):
            #     continue
            print(neighbor)
    except Exception as e:
        print(e)
