#!/usr/bin/env python3
import pandas as pd
from hearthstone import deckstrings
from hearthstone.deckstrings import Deck
from hearthstone.enums import FormatType
import random
import os


def yogg_mage():
	decktemplate = ['[(38418, 2),', '(52639, 2),', '(52706, 2),', '(38505, 1),', '(43419, 1),']
	fakedeck = [38418, 52639, 52706, 38505, 43419]
	data = pd.read_csv('hearth.csv')
	mage_spells = data.loc[(data['Type'] == 1) & (data['Minion'] == 0) & (data['Legendary'] == 0)]
	ID = mage_spells['Card ID']
	spell_value = ID.values.tolist()
	while len(decktemplate) < 16:
		card = random.choice(spell_value)
		if card not in fakedeck:
			if len(decktemplate) == 15:
				decktemplate.append("(%s, 2)]" % str(card))
				fakedeck.append(card)
			else:
				decktemplate.append("(%s, 2)," % str(card))
				fakedeck.append(card)
		else:
			print('hey')
			pass
	string = ''.join(decktemplate)
	deck = Deck()
	deck.heroes = [637]
	deck.cards = eval(string)
	deckcode = deck.as_deckstring
	cmd = "mosquitto_pub -h '192.168.5.202' -t 'hearthstone' -m '%s'" % deckcode
	os.system(cmd)
yogg_mage()
