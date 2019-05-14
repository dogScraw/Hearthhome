#!/usr/bin/env python3

from flask import Flask, request, render_template, abort, Response, redirect, url_for
import pandas as pd
from hearthstone import deckstrings
from hearthstone.deckstrings import Deck
from hearthstone.enums import FormatType
import random
import os
import time

def yogg_mage():
	#Cards that are already in deck
	decktemplate = ['[(38418, 2),', '(52639, 2),', '(52706, 2),', '(38505, 1),', '(43419, 1),']
	#List that compares cards being added to ones that are already in the deck
	fakedeck = [38418, 52639, 52706, 38505, 43419]
	#reads the csv that contains all the cards and picks out the proper ones
	data = pd.read_csv('hearth.csv')
	mage_spells = data.loc[(data['Type'] == 1) & (data['Minion'] == 0) & (data['Legendary'] == 0)]
	ID = mage_spells['Card ID']
	#converts the card IDs of the cards selected to a list
	spell_value = ID.values.tolist()
	#Picks and random card and appends it to the decktemplate list if it doesn't exist in the decktemplate list
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
			pass
	#Converts list to string
	string = ''.join(decktemplate)
	deck = Deck()
	deck.heroes = [637]
	deck.cards = eval(string)
	#Converts it to a hearthstone deckstring 
	deckcode = deck.as_deckstring
	#Posts it to the mosquitto server
	cmd = "mosquitto_pub -h '192.168.5.202' -t 'hearthstone' -m '%s'" % deckcode
	os.system(cmd)
	return(deckcode)

deckers = yogg_mage()

app = Flask(__name__)


@app.route('/')
def index():
	return render_template('index.html')

@app.route("/yoggcode/", methods=['POST'])
def move_forward():
    return render_template('index.html', value=yogg_mage())

@app.route("/druidcode/", methods=['POST'])
def move_forward2():
    return render_template('index.html', value2=yogg_mage())

if __name__ == "__main__":
        app.run(host='localhost', debug=True)
