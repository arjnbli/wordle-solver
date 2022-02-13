class Words:
    def __init__(self, path):
        # self.word_dict = self.load_words(path)
        self.words_dict = self.get_words_dict(path)
    
    def get_words_dict(self, path):
        words_dict = {}
        words_list = self.get_valid_words(path)
        for word in words_list:
            word_length = len(word)
            if word_length not in words_dict:
                words_dict[word_length] = [word]
            else:
                words_dict[word_length].append(word)
        return words_dict

    
    def get_valid_words(self, path):
        valid_chars = set('abcdefghijklmnopqrstuvwxyz')
        with open(path, 'r') as file:
            valid_words = []
            for line in file:
                word = line.lower().strip()
                is_valid = True
                for char in word:
                    if char not in valid_chars:
                        is_valid = False
                        break
                if is_valid:
                    valid_words.append(word)
        return valid_words
                

        



if __name__ == '__main__':
    words = Words('words.txt').words_dict
    print(words[5])



