
class WordleState:
    def __init__(self, word_length=5):
        self.word_length = word_length
        self.allowed_lists = None
        self.full_yellow_requirements = None
        self.__answer = None
        self.previous_guesses: list[list[dict]] = []

    def add_guess(self, word: str, correctness: list[int]=None):
        """
        Adds a guess to the word state

        :param word: The guess word string
        :param correctness: List of gray/orange/green for the guessed word, where gray=0, orange=1, green=2.
        :return:
        """

        if self.__answer is not None:
            if correctness is not None:
                raise Exception(f"ERROR: When adding word to wordstate, correctness data given when answer already provided {word=} {self.__answer=} {correctness=}")
            correctness = [-1] * self.word_length

            available_letters = list(self.__answer)
            for i, letter in enumerate(word):
                if letter == self.__answer[i]:
                    correctness[i] = 2
                    available_letters[i] = ""
                elif letter not in self.__answer:
                    correctness[i] = 0

            for i, letter in enumerate(word):
                if correctness[i] == -1:
                    if letter in available_letters:
                        correctness[i] = 1
                        available_letters.remove(letter)
                    else:
                        correctness[i] = 0

        elif correctness is None:
                raise Exception(f"ERROR: WHen adding word to wordstate, no correctness data or answer was provided. {word=} {self.__answer=} {correctness=}")

        assert (len(word) == self.word_length)
        assert (len(correctness) == self.word_length)

        new_data = []
        for i in range(self.word_length):
            new_data.append({
                "letter": word[i],
                "type": correctness[i]
            })
        self.previous_guesses.append(new_data)
        # TODO: update to cache the previous compilation and reuse it
        self.compile_prev_data()

    def set_guess_data(self, guess_data: list[list[dict]]):
        self.previous_guesses = guess_data
        self.compile_prev_data()

    def reset_guesses(self):
        self.set_guess_data([])

    def set_answer(self, answer):
        self.__answer = answer

    def check_word_valid(self, word) -> bool:
        if len(word) != self.word_length:
            return False
        if self.allowed_lists is None:
            return True

        for i,letter in enumerate(list(word)):
            if letter not in self.allowed_lists[i]:
                return False

        for req in self.full_yellow_requirements:
            if word.count(req["letter"]) < req["count"]:
                return False
            for i, letter in enumerate(list(word)):
                if letter == req["letter"] and i in req["not_at"]:
                    return False
        return True

    def filter_valid_words(self, word_list):
        return list(filter(self.check_word_valid, word_list))

    def compile_prev_data(self):
        self.allowed_lists = [
            set([chr(code) for code in range(97, 123)])
            for l in range(self.word_length)
        ]
        self.full_yellow_requirements = []

        for word in self.previous_guesses:
            yellow_requirements = []
            for i, letter in enumerate(word):
                if letter["type"] == 0:
                    self.allowed_lists[i].discard(letter["letter"])
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
                    self.allowed_lists[i] = set(letter["letter"])

            for i, letter in enumerate(word):
                if letter["type"] == 0:
                    yellow_exists = False
                    for req in yellow_requirements:
                        if req["letter"] == letter["letter"]:
                            yellow_exists = True
                    if not yellow_exists:
                        for j, allowed_list in enumerate(self.allowed_lists):
                            if word[j]["type"] != 2:
                                allowed_list.discard(letter["letter"])

            self.full_yellow_requirements += yellow_requirements

    def copy(self):
        copy_state = WordleState(self.word_length)

        for guess in self.previous_guesses:
            word = ""
            correctness = []
            for item in guess:
                word += item["letter"]
                correctness.append(item["type"])
            copy_state.add_guess(word, correctness)
        copy_state.set_answer(self.__answer)

        return copy_state
