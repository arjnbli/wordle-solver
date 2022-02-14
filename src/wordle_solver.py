from wordle_utils import Words, WordleRow, KeyBoard

class WordleSolver:
    def __init__(self, path, target_word='hello'):
        self.words = Words(path)
        self.target_word = self.validate_input(target_word)
        self.word_length = len(target_word)
        self.num_guesses = 0
        self.max_guesses = self.word_length + 1
        self.row = WordleRow(self.word_length)
        self.char_frequency = self.get_char_frequency(self.target_word)
        self.key_board = KeyBoard()
        self.guesses = []

    def validate_input(self, target_word):
        if target_word not in self.words.words_set:
            raise(ValueError('Invalid input word: {}'.format(target_word)))
        return target_word
    
    def solve(self):
        while self.num_guesses < self.max_guesses:
            if self.num_guesses == 0:
                guess = self.generate_initial_guess()
            else:
                guess = self.generate_guess()
            self.guesses.append(guess)
            self.update_row(guess)
            self.num_guesses += 1
            if guess == self.target_word:
                print('Target Word: {}, Guesses: {}'.format(self.target_word, self.guesses, self.num_guesses))
                return self.num_guesses
        print('Target Word: {}, Guesses: {}'.format(self.target_word, self.guesses, self.num_guesses))
        return -1
    
    def generate_initial_guess(self):
        import random
        words_list = self.words.words_dict[self.word_length]
        idx = random.randrange(0, len(words_list))
        return words_list[idx]
    
    def generate_guess(self):
        import random
        valid_guesses = {}
        words_list = self.words.words_dict[self.word_length]
        for word in words_list:
            is_valid = True
            for i, char in enumerate(word):
                if char in self.key_board.not_in_word:
                    is_valid = False
                    break
                if i in self.key_board.correctly_guessed and char != self.key_board.correctly_guessed[i]:
                    is_valid = False
                    break
            for char in self.key_board.in_word:
                if char not in word:
                    is_valid = False
                    break
            if is_valid:
                num_unique_letters = len(set(word))
                if num_unique_letters not in valid_guesses:
                    valid_guesses[num_unique_letters] = [word]
                else:
                    valid_guesses[num_unique_letters].append(word)
        max_unique_letters = max(valid_guesses.keys())
        idx = random.randrange(0, len(valid_guesses[max_unique_letters]))
        return valid_guesses[max_unique_letters][idx]

    def update_row(self, guess):
        indices = {'correctly_guessed': {}, 'in_word': {}, 'not_in_word': {}}
        for i in range(len(guess)):
            if self.row.cells[i].char != ' ':
                continue
            if guess[i] == self.target_word[i]:
                indices['correctly_guessed'][i] = guess[i]
                self.key_board.correctly_guessed[i] = guess[i]
                if guess[i] in self.char_frequency:
                    self.update_char_frequency(guess[i])

        for i in range(len(guess)):
            if self.row.cells[i].char != ' ':
                continue
            if guess[i] != self.target_word[i]:
                if guess[i] in self.char_frequency:
                    indices['in_word'][i] = guess[i]
                    self.key_board.in_word.add(guess[i])
                    self.update_char_frequency(guess[i])
                else:
                    indices['not_in_word'][i] = guess[i]
                    if guess[i] in self.key_board.in_word or guess[i] in set(self.key_board.correctly_guessed.values()):
                        continue
                    self.key_board.not_in_word.add(guess[i])
        
        self.row.update_domains_correctly_guessed(indices['correctly_guessed'])
        self.row.update_domains_in_word(indices['in_word'])
        self.row.update_domains_not_in_word(indices['not_in_word'])

    def update_char_frequency(self, char):
        if self.char_frequency[char] == 1:
            del self.char_frequency[char]
        else:
            self.char_frequency[char] -= 1

    @staticmethod
    def get_char_frequency(word):
        hash_table = {}
        for char in word:
            if char not in hash_table:
                hash_table[char] = 1
            else:
                hash_table[char] += 1
        return hash_table

if __name__ == '__main__':
    target_word = input('Please provide a word: ').lower()
    solver = WordleSolver('./data/words.txt', target_word)
    solver.solve()