from wordle_solver import WordleSolver
from wordle_utils import Words

def main():
    wordle_allowed = Words('./data/wordle-allowed-guesses.txt')
    wordle_answers = Words('./data/wordle-answers-alphabetical.txt')
    for word in wordle_answers.words_set:
        if word not in wordle_allowed.words_set:
            wordle_allowed.words_set.add(word)
            wordle_allowed.words_dict[len(word)].append(word)
    
    with open('./data/wordle-all-allowed-words.txt', 'w+') as file:
        for word in wordle_allowed.words_set:
            file.write(word + '\n')
    
    num_solved = 0
    num_guesses = 0
    for word in wordle_answers.words_set:
        solver = WordleSolver('./data/wordle-all-allowed-words.txt', word)
        result = solver.solve()
        if result != -1:
            num_solved += 1
            num_guesses += solver.num_guesses
    average_guesses = num_guesses / num_solved
    print('{} solved out of {}. Average Guesses = {}'.format(num_solved, len(wordle_answers.words_set), average_guesses))



if __name__ == '__main__':
    main()