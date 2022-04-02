vocabulary = [
    "a",
    "à",
    "b",
    "c",
    "ç",
    "d",
    "e",
    "è",
    "é",
    "f",
    "g",
    "h",
    "i",
    "í",
    "ï",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "ò",
    "ó",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "ú",
    "ü",
    "v",
    "w",
    "x",
    "y",
    "z",
]

extra_chars = ["-", "·", "'", " "]


def normalize(word: str) -> str:
    return (
        word.strip()
        .lower()
        .replace("à", "a")
        .replace("è", "e")
        .replace("é", "e")
        .replace("í", "i")
        .replace("ï", "i")
        .replace("ò", "o")
        .replace("ó", "o")
        .replace("ú", "u")
        .replace("ü", "u")
    )
