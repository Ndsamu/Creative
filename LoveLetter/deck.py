from random import shuffle
from card import *

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
	def discard_top(self):
		self.dis_cards.append(self.act_cards[0])
		self.act_cards.remove(self.act_cards[0])