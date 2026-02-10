import random
from WordleState import WordleState
from word_loader import load_words
from CustomerSolverAlgBase import CustomerSolverAlgBase
from SimpleSolverAlg import SimpleSolverAlg
import tqdm

def test_solver(answer_word, solver_class, word_list):
    state = WordleState()
    state.set_answer(answer_word)
    solver = solver_class(word_length=len(answer_word))
    for g in range(6):
        guess = solver.get_best_word(state.copy(), word_list)
        assert(guess in word_list)
        state.add_guess(guess)
        if guess == answer_word:
            return g+1
    return -1

def generate_sample(word_list, sample_size):
    if sample_size>len(word_list):
        return word_list[:]
    available_words = word_list[:]
    sample = []
    for i in range(sample_size):
        sample.append(available_words.pop(
            random.randint(0, len(available_words)-1)
        ))
    return sample



def main():
    random.seed(2)
    sample_size = 100
    # solver_class = CustomerSolverAlgBase
    solver_class = SimpleSolverAlg

    word_list = load_words(5)

    sample = generate_sample(word_list, sample_size)

    data = []
    for i in tqdm.trange(sample_size):
        data.append(test_solver(sample[i], solver_class, word_list))

    failed = 0
    successes = []
    for d in data:
        if d == -1:
            failed += 1
        else:
            successes.append(d)

    best = min(successes)
    worst = max(successes)
    mean = sum(successes)/len(successes)
    success_percentage = (1-failed/len(sample))*100

    print(list(zip(sample, data)))

    print("--- Results ---")
    print(f"Wordle games played: {len(sample)}/{len(word_list)}")
    print(f"Success Rate: {success_percentage:.1f}%")
    print(f"Mean guesses: {mean:.2f}")



if __name__ == "__main__":
    main()