"""
CSSE1001 Assignment 1
Semester 2, 2020
"""

from a1_support import *

# Fill these in with your details
__author__ = "{{Virat Chaudhary}} ({{s4641144}})"
__email__ = "v.chaudhary@uqconnect.edu.au"
__date__ = "3 September 2020"

# Write your code here (i.e. functions)

def select_word_at_random(word_select):

	'''
	A word string is randomely selected from WORDS_FIXED.txt or WORDS_ARBITRARY.txt based on user selection

		Parameters:
			word_select (str): Difficulty selected by user

		Returns:
			word (str): The random word that is to be guessed in the game
	'''

	if word_select == 'FIXED' or word_select == 'ARBITRARY':
		words = load_words(word_select)
		word_index = random_index(words)
		word = words[word_index]
		return word
	else:
		return None

def get_guess_index_tuple(word_length):

	'''
	Identifies the specifc subtuple used for each step of the guess sequence dependant on the word length.

		Parameters:
			word_length (int): Length of the random word to be guessed

		Returns:
			guess_tuple (tuple<tuple<int,int>>): Guess sequence tuple specific to word length
	'''

	if word_length == 6:
		guess_tuple = GUESS_INDEX_TUPLE[0]
	elif word_length == 7:
		guess_tuple = GUESS_INDEX_TUPLE[1]
	elif word_length == 8:
		guess_tuple = GUESS_INDEX_TUPLE[2]
	elif word_length == 9:
		guess_tuple = GUESS_INDEX_TUPLE[3]	
			
	return guess_tuple

def create_guess_line(guess_no, word_length):

	'''
	Generates the string representing the display corresponding to the specific guess number.

		Parameters:
			guess_no (int): The guess number the user is currently on
			word_length (int): Length of the random word to be guessed 

		Returns:
			output_str (str): The guess display for the guess number
	'''

	word_guess_tuple = get_guess_index_tuple(word_length)
	current_guess_subtuple = word_guess_tuple[guess_no - 1]
	lowest_index, highest_index = current_guess_subtuple

	output_str = ''
	output_str += 'Guess {}{}'.format(guess_no, WALL_VERTICAL)

	for i in range(word_length):
		if i >= lowest_index and i <= highest_index:
			output_str += ' * {}'.format(WALL_VERTICAL)
		else:
			output_str += ' {} {}'.format(WALL_HORIZONTAL, WALL_VERTICAL)

	return output_str

def display_guess_matrix(guess_no, word_length, scores):

	'''
	Shows the progress of the game upto and including the current guess number and scores for the previous guesses made

		Parameters:
			guess_no (int): The guess number the user is currently on 
			word_length (int): Length of the random word to be guessed 
			scores (tuple<int>): Scores for all the previous guesses

		Prints:
			Guess Matrix: Displays the entire matrix to indicate the progress of the game
	'''

	display_header_str = (' ' * 7) + WALL_VERTICAL
	for i in range(word_length):
		display_header_str += ' {} {}'.format(i + 1,WALL_VERTICAL)

	horizontal_seperator = WALL_HORIZONTAL * (len(display_header_str) + 1)

	print(display_header_str)
	print(horizontal_seperator)

	for i in range(guess_no):
		if i + 1 == guess_no:
			print(create_guess_line(i + 1, word_length))
		else:
			print(create_guess_line(i + 1, word_length) + '   {} Points'.format(scores[i]))
		
		print(horizontal_seperator)

def compute_value_for_guess(word, start_index, end_index, guess):

	'''
	Calculates the score, an integer, the player is awarded for the specific guess made.

		Parameters: 
			word (str): The random word that is to be guessed in the game
			start_index (int): The index of the word from which the guess is to be considered for scoring
			end_index (int): The index of the word upto and including to which to guess is to be considered for scoring
			guess (str): The guess for the specifc guess number that is made by the user

		Returns:
			score (int): The score received by the user for the guess made 
	'''

	score = 0
	correct_guess = word[start_index:end_index + 1]

	for i in range(len(guess)):
		if guess[i] == correct_guess[i] and guess[i] in VOWELS:
			score += 14
		elif guess[i] == correct_guess[i] and guess[i] in CONSONANTS:
			score += 12
		elif guess[i] in correct_guess:
			score += 5
		else:
			score += 0
	
	return score

def main():
	"""
	Handles top-level interaction with user.
	"""
	# Write the code for your main function here

	print(WELCOME)
	
	while True: 

		# This while loop handles the initial program startup prompt where the user selects to start, help or quit.	

		print(INPUT_ACTION, end='')

		choice = input('')

		if choice == 's':
			break
		elif choice == 'h':
			print(HELP)
			break
		elif choice == 'q':
			return
		else:
			print(INVALID)
			
	while True:		

		# This while loop handles the user input for word difficulty, either 'FIXED' or 'ARBITRARY' must be selected. 

		word_select = input("Do you want a 'FIXED' or 'ARBITRARY' length word?: ")
		word = select_word_at_random(word_select)
		if word != None:
			break	

	guess_no = 1
	word_length = len(word)
	scores = ()

	while guess_no <= word_length:

		# This outer while loop iterates for each guess number, prompting the user to enter a specific guess each time. 

		if guess_no == 1:
			print('Now try and guess the word, step by step!!')
		
		display_guess_matrix(guess_no, word_length, scores)

		while True:

			'''
			This nested while loop handles the messages given to the user after each guess
			This includes the last guess after which the user is informed about their success in the game
			'''

			if guess_no == word_length:
				guess = input('Now enter your final guess. i.e. guess the whole word: ')
				if guess == word:
					print('You have guessed the word correctly. Congratulations.')
				else:
					print('Your guess was wrong. The correct word was "{}"'.format(word))
			else:
				guess = input('Now enter Guess {}: '.format(guess_no))

			'''
			This block gets the start_index and end_index of the word and checks whether
			the guess made satisfies the length of the required guess using the guess index tuple. 
			'''

			start_index, end_index = get_guess_index_tuple(word_length)[guess_no - 1]
			required_num_guess_letters = (end_index - start_index) + 1
			if len(guess) == required_num_guess_letters:
				break

		'''
		If the correct length for the guess is inputted by the user,
		then the score for the guess is calculated and added to the scores tuple.
		'''

		current_guess_score = compute_value_for_guess(word, start_index, end_index, guess)
		scores += (current_guess_score,)		
		
		guess_no += 1

if __name__ == "__main__":
	main()
