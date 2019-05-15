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

def big_druid():
	#Cards already in deck
        decktemplate = ['[(1124, 2),', '(95, 2),']
        fakedeck = [1124, 95]
        data = pd.read_csv('hearth.csv')
	#Loads cards with specific parameters
        druid_spells = data.loc[(data['Type'] == 2) & (data['Minion'] == 0) & (data['Legendary'] == 0) & (data['Cost'] < 5)]
        druidlegends = data.loc[(data['Type'] == 2) & (data['Minion'] == 1) & (data['Legendary'] == 1) & (data['Cost'] >= 5)]
        neutrallegends = data.loc[(data['Type'] == 0) & (data['Minion'] == 1) & (data['Legendary'] == 1) & (data['Cost'] >= 5)]
        neutralminions = data.loc[(data['Type'] == 0) & (data['Minion'] == 1) & (data['Legendary'] == 0) & (data['Cost'] >= 5)]
	#Takes the card ID of the selected cards and turns it into a variable
        spellsID = druid_spells['Card ID']
        druidlegendsID = druidlegends['Card ID']
        neutrallegendsID = neutrallegends['Card ID']
        neutralminionsID = neutralminions['Card ID']
	#Converts it to a list
        spell_value = spellsID.values.tolist()
        neutrallegends_value = neutrallegendsID.values.tolist()
        druidlegends_value = druidlegendsID.values.tolist()
        neutralminions_value = neutralminionsID.values.tolist()
	#Iterates over a list and adds it to the decktemplate and fakedeck to see if it already exists in the deck
        while len(decktemplate) < 7:
                card = random.choice(spell_value)
                if card not in fakedeck:
                        decktemplate.append("(%s, 2)," % str(card))
                        fakedeck.append(card)
                else:
                        pass
        while len(decktemplate) < 9:
                card = random.choice(druidlegends_value)
                if card not in fakedeck:
                        decktemplate.append("(%s, 1)," % str(card))
                        fakedeck.append(card)
                else:
                        pass
        while len(decktemplate) < 13:
                card = random.choice(neutrallegends_value)
                if card not in fakedeck:
                        decktemplate.append("(%s, 1)," % str(card))
                        fakedeck.append(card)
                else:
                        pass

        while len(decktemplate) < 18:
                card = random.choice(neutralminions_value)
                if card not in fakedeck:
                        if len(decktemplate) == 17:
                                decktemplate.append("(%s, 2)]" % str(card))
                                fakedeck.append(card)
                        else:
                                decktemplate.append("(%s, 2)," % str(card))
                                fakedeck.append(card)
                else:
                        pass

        #Converts list to string
        string = ''.join(decktemplate)
	#Adds cards and hero to the Deck()
        deck = Deck()
        deck.heroes = [274]
        deck.cards = eval(string)
        #Converts it to a hearthstone deckstring 
        deckcode = deck.as_deckstring
        #Posts it to the mosquitto server
        cmd = "mosquitto_pub -h '192.168.5.202' -t 'hearthstone' -m '%s'" % deckcode
        os.system(cmd)
        return(deckcode)

