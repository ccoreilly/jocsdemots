from tqdm import tqdm


def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError


def levenshtein(a, b):
    "Calculates the Levenshtein distance between a and b."
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a, b = b, a
        n, m = m, n

    current = list(range(n + 1))
    for i in range(1, m + 1):
        previous, current = current, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete = previous[j] + 1, current[j - 1] + 1
            change = previous[j - 1]
            if a[j - 1] != b[i - 1]:
                change = change + 1
            current[j] = min(add, delete, change)

    print(f"Distance of {a} and {b}: {current[n]}")

    return current[n]


def prune_fasttext_vectors(
    original_filepath: str, pruned_filepath: str, words: set[str]
):
    with open(original_filepath) as vector_file:
        with open(pruned_filepath, "w") as write_file:
            for line in tqdm(vector_file):
                if line == "2000000 300":
                    continue
                fasttext_data = line.split()
                fasttext_word = fasttext_data[0]
                if fasttext_word not in words:
                    continue
                write_file.write(line)
