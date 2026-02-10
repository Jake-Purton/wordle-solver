import pathlib

def load_words(word_length=5):
    current = pathlib.Path(__file__).parent.resolve()
    with open(current / "words_alpha.txt", "r") as f:
        all_words = f.read().split()

    filtered_words = []
    for word in all_words:
        word = word.strip()
        if len(word) == word_length:
            filtered_words.append(word)

    return filtered_words
