#!/usr/bin/env python3
import pandas as pd
from hearthstone import deckstrings
from hearthstone.deckstrings import Deck
from hearthstone.enums import FormatType
import random
import paho.mqtt.client as mqtt
import os

broker = '192.168.5.202'
client = mqtt.Client()


def yogg_mage():
	decktemplate = ['[(38418, 2),', '(52639, 2),', '(52706, 2),', '(38505, 1),', '(43419, 1),']
	data = pd.read_csv('hearth.csv')
	mage_spells = data.loc[(data['Type'] == 1) & (data['Minion'] == 0) & (data['Legendary'] == 0)]
	ID = mage_spells['Card ID']
	spell_value = ID.values.tolist()
	for i in range(1, 12):
		card = random.choice(spell_value)
		#if card in list:
		#else:
		if i == 11:
			decktemplate.append("(%s, 2)]" % str(card))
		else:
			decktemplate.append("(%s, 2)," % str(card))
	string = ''.join(decktemplate)
	deck = Deck()
	deck.heroes = [637]
	deck.cards = eval(string)
	deckcode = deck.as_deckstring
	cmd = "mosquitto_pub -h '192.168.5.202' -t 'hearthstone' -m '%s'" % deckcode
	os.system(cmd)

yogg_mage()
