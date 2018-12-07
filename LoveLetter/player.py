from defs import *

class Player:

	def __init__(self, name, hand):
		self.name = name
		self.hand = hand
		self.wins = 0
		self.handmaiden = False
		self.status = True

	# Returns the card with the highest strength
	def max_card(self):
		max_card = self.hand[0]
		for card in self.hand:
			if card.strength > max_card.strength:
				max_card = card
		return max_card
	
	# Returns a cardname in string format
	def select_card(self):
		print("\nPlease enter card: ")
		cardname = input().lower()
		# THIS needs to be changed to check against only the players hand (i.e. player's cardnames)
		while cardname not in cardnames:
			self.show_name()
			self.show_cards()
			clear_console()
			print("\nInvalid. Please enter card: ")
			cardname = input().lower()
		print(newline_sm)
		return cardname

	# Returns a player NAME (string)
	def select_target(self, player_names):
		print("\nSelect target: ")
		target = input()
		while (target not in player_names):
			print("\nInvalid input. Select target: ")
			target = input()
		return target

	# Handles user's turns by prompting their name and cards
	def turn(self):
		self.show_name()
		self.show_cards()
		card = self.play_card()
		return card

	# Returns actual card object
	def play_card(self):
		cardname = self.select_card()
		for card in self.hand:
			if card.name == cardname:
				card_out = card
				self.hand.remove(card)
				return card_out
		else:
			return None

	# Default (selects first card) for debugging
	def def_play(self):
		card = self.hand[0]
		self.hand.remove(card)
		return card

	# Following two functions form the user_prompt

	def show_name(self):
		print("\n%s" % self.name)
		print("-----------")

	def show_cards(self):
		print("Cards: ")		
		for card in self.hand:
			print("%s" % card.name)
		print("\n")

	# Print out username and their hand
	def user_prompt(self):
		self.show_name()
		self.show_cards()

