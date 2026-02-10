from word_loader import load_words

class WordleManager:
    def __init__(self, solver_class, word_length=5):
        self.word_length = word_length

        self.word_list = load_words(5)

        self.solver = solver_class(word_length)

    def get_best_words(self, prev_words: list[list[dict]]):

        validator = WordValidator(prev_words, self.word_length)

        possible_words = []

        for word in self.word_list:
            if validator.check_word(word):
                possible_words.append(word)

        evaluator = WordEvaluator(possible_words, self.word_length)

        possible_words.sort(key=evaluator.evaluate_word, reverse=True)

        return possible_words

