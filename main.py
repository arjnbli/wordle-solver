from utils import Words, WordleRow, WordleCell, KeyBoard

class WordleSolver:
    def __init__(self, target_word, path):
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
            raise(ValueError('Invalid input word'))
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
                return self.num_guesses
        return -1
    
    def generate_initial_guess(self):
        return 'crane'
    
    def generate_guess(self):
        '''
        TODO
        [x] Iterate through all words with same length as target
        [] A word can be a possible solution if 
            [x] It contains all the correctly guessed letters so far in the correct position 
            [x] It doesn't contain a character that is not in the word
            [] It contains characters known to be in the word
        [x] Add a word that passes these checks to the list of possible next guesses
        [x] Randomly select from one of the guesses
        '''
        import random
        valid_guesses = []
        word_list = self.words.words_dict[self.word_length]
        for word in word_list:
            is_valid = True
            count = 0
            for i, char in enumerate(word):
                if char in self.key_board.not_in_word:
                    is_valid = False
                    break
                if i in self.key_board.correctly_guessed and char != self.key_board.correctly_guessed[i]:
                    is_valid = False
                    break
                if char in self.key_board.in_word:
                    count += 1
            if count != len(self.key_board.in_word):
                is_valid = False
            if is_valid:
                valid_guesses.append(word)
        idx = random.randrange(0, len(valid_guesses))
        return valid_guesses[idx]

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
                    
        print(self.guesses[-1], indices)
        print(self.key_board)
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
    #target_word = input('Please provide a word: ').lower()
    target_word = 'scary'
    solver = WordleSolver(target_word, 'words.txt')
    print(target_word)
    solver.solve()
    print(solver.guesses)
    # print(solver.generate_guess())