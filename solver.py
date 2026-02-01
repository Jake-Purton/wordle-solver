import pathlib


class WordleSolver:
    def __init__(self, word_length=5):
        self.word_length = word_length
        current = pathlib.Path(__file__).parent.resolve()
        with open(current / "words_alpha.txt", "r") as f:
            all_words = f.read().split()

        self.word_list = []
        for word in all_words:
            word = word.strip()
            if len(word) == self.word_length:
                self.word_list.append(word)

    def get_best_words(self, prev_words: list[list[dict]]):

        validator = WordValidator(prev_words, self.word_length)

        possible_words = []

        for word in self.word_list:
            if validator.check_word(word):
                possible_words.append(word)

        evaluator = WordEvaluator(possible_words)

        possible_words.sort(key=evaluator.evaluate_word, reverse=True)

        return possible_words

class WordValidator:
    def __init__(self, prev_words, word_length):
        self.word_length = word_length
        self.prev_words = prev_words
        self.allowed_list, self.full_yellow_requirements = self.compile_prev_data(prev_words)

    def check_word(self, word) -> bool:
        for i,letter in enumerate(list(word)):
            if letter not in self.allowed_list[i]:
                return False

        for req in self.full_yellow_requirements:
            if word.count(req["letter"]) < req["count"]:
                return False
            for i, letter in enumerate(list(word)):
                if letter == req["letter"] and i in req["not_at"]:
                    return False

        return True

    def compile_prev_data(self, prev_words):
        allowed_lists = [
            set([chr(code) for code in range(97, 123)])
            for l in range(self.word_length)
        ]
        full_yellow_requirements = []

        for word in prev_words:
            yellow_requirements = []
            for i, letter in enumerate(word):
                if letter["type"] == 0:
                    for allow_list in allowed_lists:
                        allow_list.discard(letter["letter"])
                elif letter["type"] == 1:
                    letter = letter["letter"]
                    for req in yellow_requirements:
                        if req["letter"] == letter:
                            req["not_at"].add(i)
                            req["count"] += 1
                            continue
                    yellow_requirements.append({
                        "letter": letter,
                        "not_at": {i},
                        "count": 1
                    })
                elif letter["type"] == 2:
                    allowed_lists[i] = set(letter["letter"])

            full_yellow_requirements += yellow_requirements

        return allowed_lists, full_yellow_requirements

class WordEvaluator:
    def __init__(self, word_list):
        self.letter_values = self.get_letter_values(word_list)

    def evaluate_word(self, word):
        total = 0
        used = set()
        for letter in word:
            if letter in used:
                continue
            total += self.letter_values[letter]
            used.add(letter)
        return total

    def get_letter_values(self, word_list):
        dict = {}
        for word in word_list:
            for letter in word:
                if letter in dict:
                    dict[letter] += 1
                else:
                    dict[letter] = 1
        return dict

