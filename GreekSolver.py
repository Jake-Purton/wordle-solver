
from CustomerSolverAlgBase import CustomerSolverAlgBase
from WordleState import WordleState

class GreekSolver(CustomerSolverAlgBase):
    def __init__(self, word_length, word_list):
        # TODO add word list here and remove invalid ones to make future search faster

        self.word_list = list(word_list)
        if "raise" in self.word_list:
            self.word_list.remove("raise")

        self.word_length = word_length

    def _compute_correctness(self, guess, answer):
        correctness = [-1] * self.word_length
        available_letters = list(answer)

        for i, letter in enumerate(guess):
            if letter == answer[i]:
                correctness[i] = 2
                available_letters[i] = ""
            elif letter not in answer:
                correctness[i] = 0

        for i, letter in enumerate(guess):
            if correctness[i] == -1:
                if letter in available_letters:
                    correctness[i] = 1
                    available_letters.remove(letter)
                else:
                    correctness[i] = 0

        return tuple(correctness)

    def get_valid_combos(self, game_state: WordleState, word, beta):
        maximum = 0

        # print(word)

        buckets = {}
        for answer in self.word_list:
            correctness = self._compute_correctness(word, answer)
            count = buckets.get(correctness, 0) + 1
            buckets[correctness] = count
            if count > maximum:
                maximum = count
                if maximum > beta:
                    return maximum

        return maximum
        
    def get_best_word(self, game_state):

        if len(game_state.previous_guesses) == 0 and self.word_length == 5:
            # first go is always raise (as when i ran this it decided raise was the best)
            return "raise"
            # return "crane"
            # return "audio"

        self.word_list = game_state.filter_valid_words(self.word_list)

        minimum = 10000000000
        min_word = ""

        for word in self.word_list:
            a = self.get_valid_combos(game_state, word, minimum)
            if a < minimum:
                minimum = a
                min_word = word

        return min_word
