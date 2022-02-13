class WordleSolver:
    def __init__(self, target_word, path):
        self.words = Words(path)
        self.target_word = self.validate_input(target_word)
        self.word_length = len(target_word)
        self.num_guesses = 0
        self.max_guesses = self.word_length

    def validate_input(self, target_word):
        if target_word not in self.words.words_set:
            raise(ValueError('Invalid input word'))
        return target_word
    
    def solve(self):
        pass


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
    target_word = input('Please provide a word: ').lower()
    solver = WordleSolver(target_word, 'words.txt')