from CustomerSolverAlgBase import CustomerSolverAlgBase

class SimpleSolverAlg(CustomerSolverAlgBase):
    def __init__(self, word_list, word_length=5):
        self.word_list = word_list
        super().__init__(word_length)

    def get_best_word(self, game_state):
        valid_words = game_state.filter_valid_words(self. word_list)
        self.letter_values = self.get_letter_values(valid_words)
        valid_words.sort(key=self.evaluate_word, reverse=True)
        return valid_words[0]

    def evaluate_word(self, word):
        total = 0
        used = set()
        for i, letter in enumerate(word):
            if letter in used:
                continue
            total += self.letter_values[i][letter]
            used.add(letter)
        return total

    def get_letter_values(self, word_list) -> list[dict[str, int]]:
        green_val = 3
        yellow_val = 1
        dicts = [{} for a in range(self.word_length)]
        for word in word_list:
            for i, letter in enumerate(word):
                for l in range(self.word_length):
                    if letter in dicts:
                        dicts[l][letter] += yellow_val
                    else:
                        dicts[l][letter] = yellow_val
                dicts[l][letter] += green_val
        return dicts