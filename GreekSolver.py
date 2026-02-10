
from WordleState import WordleState

class GreekSolver:
    def __init__(self, word_length):
        # TODO add word list here and remove invalid ones to make future search faster
        self.combinations = []
        for i in range(0, 3**word_length):
            list = []
            for _ in range(0,word_length):
                list.append(i%3)
                i /= 3

        self.word_length = word_length

    def get_valid_combos(self, game_state: WordleState, word, word_list):
        combos = self.combinations.copy()

        maximum = 0

        for combo in combos:
            current_state = game_state.copy()
            current_state.add_guess(word, combo)
            maximum = max(len(current_state.filter_valid_words(word_list)), maximum)

        return maximum
        
    def get_best_word(self, game_state, word_list):

        valid_words = game_state.filter_valid_words(word_list)

        minimum = 10000000000
        min_word = ""

        print(len(valid_words))

        for word in valid_words:
            a = self.get_valid_combos(game_state, word, word_list)
            if a < minimum:
                minimum = a
                min_word = word

        # print(min_word)

        return min_word
