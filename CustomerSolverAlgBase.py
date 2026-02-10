

class CustomerSolverAlgBase:
    def __init__(self, word_length):
        self.word_length = word_length

    def get_best_word(self, game_state, word_list):
        valid_words = game_state.filter_valid_words(word_list)
        return valid_words[0]
