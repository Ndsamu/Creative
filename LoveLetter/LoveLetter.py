from random import shuffle

cardnames = ["guard", "priest", "baron", "handmaiden", "prince", "king", "countess", "princess"]
modes = ["debug", "standard"]
newline_lg = "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
newline_sm = "\n\n"

#TODO: Better organize functions and hierarchy, Implement rest of card effects, Better input handling,
###### List cards when prompting user to select an option, Implement invincibity w/ Handmaiden,
###### Implement functionality for full games (multiple rounds, up to a specified user input: 3-7)

#FUTURE: Add a GUI or at the very least a better representation of cards in ASCII art or something
########

class Card:

	def __init__(self, name, strength):
		self.name = name
		self.strength = strength

class Deck:

	def __init__(self,cards):
		self.act_cards = cards
		self.dis_cards = []
	
	def show_cards(self):
		for card in self.act_cards:
			print(card.name)

	def shuffle(self):
		shuffle(self.act_cards)

	def reset(self):
		self.act_cards.extend(self.dis_cards)
		self.shuffle()

	def deal_card(self):
		card = self.act_cards[0]
		self.act_cards.remove(card)
		return card

	def discard(self, card):
		self.dis_cards.append(card)

	# Prevents individuals from using process of elimination to deduct final cards
	def rem_top(self):
		self.dis_cards.append(self.act_cards[0])
		self.act_cards.remove(self.act_cards[0])

class Player:

	def __init__(self, name, hand):
		self.name = name
		self.hand = hand
		self.wins = 0
		self.handmaiden = False
		self.status = True

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

	# Following two processes form the user_prompt
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

class Game:

	def __init__(self, num_players, players, deck):
		self.num_players = num_players
		self.act_players = players
		# Potentially used to reinstate player order:
		# self.players_cpy = players
		self.out_players = []
		self.deck = deck
		self.game_status = True
		self.round_status = True

	# (Work in Progress)
	def check_game_status(self):
		print("Checking game status")

	# PLAYER METHODS

	# Removes player from active players
	def rem_player(self, player):
		tmp = player
		self.act_players.remove(tmp)
		self.out_players.append(tmp)

	# Returns a player object by searching for their name
	def get_player(self, name):
		for player in self.act_players:
			if player.name == name:
				return player
		else:
			return

	# Returns a list of active player names (STRINGS) (for interaction between players)
	def get_player_names(self):
		nmlist = []
		for player in self.act_players:
			nmlist.append(player.name)

		return nmlist

	# Returns the index of a player given a player object
	def get_player_index(self, player):
		for i in range(0,len(self.act_players)):
			if player.name == self.act_players[i]:
				return i
		else:
			return -1

	def reset_handmaiden(self):
		for player in self.act_players:
			player.handmaiden = False

	# GAME METHODS

	# Checks for the two possible conditions (1 user left or no more cards)
	# returns true if the round is still active and false otherwise
	def check_round_status(self):
		self.update_act_players()
		if not self.deck.act_cards:
			self.empty_deck()
			return False
		if len(self.act_players) == 1:
			print("Winner! Congratulations %s.\n\n" % self.act_players[0].name)
			return False
		return True

	# Deals one card to the specified player
	def deal(self, player):
		player.hand.append(self.deck.deal_card())

	# Deals one card to every player
	def deal_all(self):
		for player in self.act_players:
			self.deal(player)

	# Checks the status of all players and kicks them as needed
	def update_act_players(self):
		for player in self.act_players:
			if not player.status:
				self.rem_player(player)

	# Handles the situation in which the game deck is empty (End of Round)
	def empty_deck(self):
		top_player = self.compare_cards()
		top_idx = self.get_player_index(top_player)
		self.act_players.remove(top_player)
		sec_player = self.compare_cards()
		self.act_players.insert(top_idx, top_player)
		clear_console()
		print("Top Player: %s \nCard: %s\n" % (top_player.name, top_player.max_card().name))
		print("Sec Player: %s \nCard: %s\n" % (sec_player.name, sec_player.max_card().name))
		if top_player.max_card().strength == sec_player.max_card().strength:
			print("Draw! Tie between player %s and %s." % (top_player.name, sec_player.name))
			return
		else:
			print("Winner! Congratulations %s.\n\n" % top_player.name)
			return top_player

	# Compares the cards of active players for the highest scoring card (in case of empty deck)
	def compare_cards(self):
		top_strength = 0
		for player in self.act_players:
			tmp_strength = player.max_card().strength
			if tmp_strength > top_strength:
				top_strength = tmp_strength
				top_player = player
		return top_player

	# Will have a switch case for selecting appropriate func. call
	def exec_card(self, player):
		card = player.play_card()
		#print("Cardname %s" % card.name)
		if card.name == "guard":
			self.guard(player)
		elif card.name == "priest":
			self.priest(player)
		elif card.name == "baron":
			self.baron(player)
		return card

	def prompt_targets(self, player, msg):
		clear_console()
		print("Targets: ")
		targets = self.get_player_names()
		targets.remove(player.name)
		print(', '.join(targets))
		print(msg)
		target = self.get_player(player.select_target(self.get_player_names()))
		while target not in self.act_players and not target.handmaiden:
			print("\nInvalid player selection")
			target = self.get_player(player.select_target(self.get_player_names()))
		return target
		

	def guard(self, player):
		target = self.prompt_targets(player, "\nGuess player's card from selection: ")
		print(', '.join(cardnames))
		guess = player.select_card()
		while guess == "guard":
			print("Cannot select guard as target of guard")
			guess = player.select_card()
		for card in target.hand:
			if guess == card.name:
				target.status = False
				print("\nCorrect! Player eliminated\n")
				break
		else:
			print("Incorrect.")
	
	def priest(self, player):
		target = self.prompt_targets(player, "Choose a player to view their cards:")
		print(newline_sm)
		print("Player %s's cards: " % target.name)
		for card in target.hand:
			print(card.name)
		print(newline_sm)

	def baron(self, player):
		target = self.prompt_targets(player, "\nChoose a player to compare your top card: ")
		print(newline_sm)
		player_card = player.max_card()
		target_card = target.max_card()
		if (player_card.strength > target_card.strength):
			target.status = False
			print("Card %s (%s) beats card %s (%s)" % (player_card.name, player.name, target_card.name, target.name))
			print("Player %s eliminated!" % target.name)
		else:
			player.status = False
			print("Card %s (%s) beats card %s (%s)\n" % (target_card.name, target.name, player_card.name, player.name))
			print("Player %s eliminated!" % player.name)
		print(newline_sm)

	#def handmaiden(self, player):
		

	# Handles invidual rounds
	def round(self):
		self.deck.reset()
		self.deck.rem_top()
		self.deal_all()
		self.deal_all()
		print("Ready to start?! (Press ENTER to continue)")
		null = input()
		clear_console()
		while(self.round_status):
			for player in self.act_players:
				print("%s's turn. No cheating... (Press ENTER to continue)" % player.name)
				null = input()
				clear_console()
				player.user_prompt()
				discard = self.exec_card(player)
				#discard = player.def_play()
				self.deck.discard(discard)
				if not self.check_round_status():
					exit()
				self.deal(player)
				self.check_round_status()
				print("Next players turn! (Press ENTER to continue)")
				null = input()
				self.reset_handmaiden()
				clear_console()

	def debug(self):
		self.deck.reset()
		self.deal_all()
		clear_console()
		while(self.round_status):
			for player in self.act_players:
				player.user_prompt()
				discard = self.exec_card(player)
				if not self.check_round_status():
					exit()
				clear_console()

#Global method for command line execution
def clear_console():
		print(newline_lg)

class init:

	def __init__(self):
		self.deck = []
		self.players = []
		self.choose_mode()

	def choose_mode(self):
		print("Please select mode [debug/standard]: ")
		mode = input().lower()
		while (mode[0] != "d" and mode[0] != "s"):
			print("Invalid choice. Please select mode [debug/standard]: ")
			mode = input().lower()
		if mode[0].lower() == "d":
			self.debug()
		else:
			self.standard()

	def debug(self):
		clear_console()
		print("Debug Mode: \n\n")
		card = Card("baron", 3)
		player1 = Player("Player1", [card])
		card = Card("baron", 3)
		player2 = Player("Player2", [card])

		game = Game(2, [player1,player2], self.gen_deck())
		game.debug()

	def standard(self):
		clear_console()
		print("LoveLetter")
		print("by Nate Samuelson")
		print("--------------------------------------------------------------------------\n\n\n\n")
		self.deck = self.gen_deck()
		num_players = int(input("Please enter the number of players: "))
		while(num_players < 2 or num_players > 4):
			num_players = int(input("Please enter the number of players: "))
		clear_console()
		for i in range(0, num_players):
			print("\nPlease enter player %d's name: " % (i+1))
			name = input()
			player = Player(name, [])
			self.players.append(player)
			clear_console()

		print('\n\nPlayers:')
		for i in range(0, num_players):
			print(" - %s" % self.players[i].name)
		print("\n\n\n")


		game = Game(num_players, self.players, self.deck)
		game.round()

	def gen_deck(self):
		cards = []
		for i in range(0,5):
			card = Card("guard", 1)
			cards.append(card)
		for i in range(0,2):
			card = Card("priest", 2)
			cards.append(card)
		for i in range(0,2):
			card = Card("baron", 3)
			cards.append(card)
		for i in range(0,2):
			card = Card("handmaiden", 4)
			cards.append(card)
		for i in range(0,2):
			card = Card("prince", 5)
			cards.append(card)
		card = Card("king", 6)
		cards.append(card)
		card = Card("countess", 7)
		cards.append(card)
		card = Card("princess", 8)
		cards.append(card)

		deck = Deck(cards)
		return deck



#LET THE FUN BEGIN!

def main():
	init()

if __name__== "__main__":
	main()

