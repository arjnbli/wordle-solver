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

class WordleCell:
    def __init__(self, char=' '):
        self.char = char
        self.domain = set('abcdefghijklmnopqrstuvwxyz')
    
    def remove_from_domain(self, char):
        if char in self.domain:
            self.domain.remove(char)
    
    def __repr__(self):
        return self.char

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

class KeyBoard:
    def __init__(self):
        self.correctly_guessed = {}
        self.in_word = {}
        self.not_in_word = {}
    
    def __repr__(self):
        return str({
        'correctly_guessed': self.correctly_guessed,
        'in_word': self.in_word,
        'not_in_word': self.not_in_word
        })