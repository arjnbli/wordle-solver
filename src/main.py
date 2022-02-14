from wordle_solver import WordleSolver
from wordle_utils import Words

def main():
    results = []
    wordle_answers = Words('./data/wordle-answers-alphabetical.txt').words_dict[5]
    for word in wordle_answers:
        solver = WordleSolver('./data/words.txt', word)
        results.append([word, solver.guesses ,solver.solve()])
    return results


if __name__ == '__main__':
    results = main()
    for result in results:
        print(result)
    