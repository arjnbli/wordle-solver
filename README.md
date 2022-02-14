# wordle-solver 

## Overview
Python module for solving the wordle game - https://www.nytimes.com/games/wordle/index.html. The goal of the game is to guess an arbitrary 5-letter word in 6
tries. If a guess doesn't match the target word, information is revealed regarding each character. If a character in the guess is in the same position as the same 
character in the target word, it is marked with green. If a character in the guess is in the target word but in the wrong position, it is marked with yellow. If a 
character in the guess is not in the target word, it is marked with black. The information provided by the hints can be leveraged to generate the next guess.

## Usage
The two files of interest in this module are - wordle_solver.py and main.py. 

The wordle_solver.py prompts the user for a target word (while the game only involves 5-letter words, this module can handle words of any length) and attempts 
to guess it in at most word_length + 1 tries (This can can adjusted). wordle-solver.py uses the words provided here -https://github.com/dwyl/english-words but
it can be configured to work with any word list by providing the path to the word file to the WordleSolver class.

The main.py file checks the performance of the wordle-solver using the words in - 
1. https://gist.github.com/cfreshman/a03ef2cba789d8cf00c08f767e0fad7b 
2. https://gist.github.com/cfreshman/cdcdf777450c5b5301e439061d29694c 

(These words extracted from the source of the wordle website itself)

## Performance
Currently, initial guesses generated are randomly chosen from the list of all words of length=target_word such that they have unique characters (in order maximize
information obtained from the subsequent hint). Guesses that are generated subsequently are randomly chosen from a subset of the total words. This subset 
is obtained by eliminating words based on the hint - words that have characters confirmed not to be in the target by the hint and words that don't have all the 
characters known to be in the target word. The performance metrics obtained by averaging the results over 10 passes through the words in the wordle-answers list
are as follows - 
1. Percentage of words guessed in 6 tries or less = 77.47%
2. Average Guesses for Words guessed in 6 tries or less = 4.81 guesses
