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
        pass

    def update_row(self, guess):
        indices = {'correctly_guessed': {}, 'in_word': {}, 'not_in_word': {}}
        for i in range(len(guess)):
            if self.row.cells[i].char != ' ':
                continue
            if guess[i] == self.target_word[i]:
                indices['correctly_guessed'][i] = guess[i]
                if guess[i] in self.char_frequency:
                    self.update_char_frequency(guess[i])
        
        for i in range(len(guess)):
            if self.row.cells[i].char != ' ':
                continue
            if guess[i] != self.target_word[i]:
                if guess[i] in self.char_frequency:
                    indices['in_word'][i] = guess[i]
                    self.update_char_frequency(guess[i])
                else:
                    indices['not_in_word'][i] = guess[i]
        print(self.guesses[-1], indices)
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

class WordleRow:
    def __init__(self, word_length):
        self.cells = [WordleCell() for i in range(word_length)]
    
    def update_domains_correctly_guessed(self, char_dict):
        for i in range(len(self.cells)):
            cell = self.cells[i]
            if i in char_dict:
                cell.domain = set([char_dict[i]])
                continue
            for char in set(char_dict.values()):
                if char in cell.domain:
                    cell.domain.remove(char)

    def update_domains_in_word(self, char_dict):
        for i in range(len(self.cells)):
            cell = self.cells[i]
            if i in char_dict and char_dict[i] in cell.domain:
                cell.domain.remove(char_dict[i])

    def update_domains_not_in_word(self, char_dict):
        for char in char_dict.values():
            for cell in self.cells:
                if char in cell.domain:
                    cell.domain.remove(char)

    def __repr__(self):
        row_vals = []
        for cell in self.cells:
            row_vals.append(cell.char)
        return str(row_vals)

class WordleCell:
    def __init__(self, char=' '):
        self.char = char
        self.domain = set('abcdefghijklmnopqrstuvwxyz')
    
    def remove_from_domain(self, char):
        if char in self.domain:
            self.domain.remove(char)
    
    def __repr__(self):
        return self.char

class KeyBoard:
    def __init__(self):
        self.in_word = set()
        self.not_in_word = set()

class Words:
    def __init__(self, path):
        self.words_set = self.get_valid_words(path)
        self.words_dict = self.get_words_dict()
        
    def get_valid_words(self, path):
        valid_chars = set('abcdefghijklmnopqrstuvwxyz')
        with open(path, 'r') as file:
            valid_words = set()
            for line in file:
                word = line.lower().strip()
                is_valid = True
                for char in word:
                    if char not in valid_chars:
                        is_valid = False
                        break
                if is_valid:
                    valid_words.add(word)
        return valid_words
    
    def get_words_dict(self):
        words_dict = {}
        words_list = list(self.words_set)
        for word in words_list:
            word_length = len(word)
            if word_length not in words_dict:
                words_dict[word_length] = [word]
            else:
                words_dict[word_length].append(word)
        return words_dict
                

if __name__ == '__main__':
    #target_word = input('Please provide a word: ').lower()
    target_word = 'scary'
    solver = WordleSolver(target_word, 'words.txt')
    print(target_word)
    solver.solve()
    print(solver.guesses)
  