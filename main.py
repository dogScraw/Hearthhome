#!/usr/bin/env python3

from flask import Flask, request, render_template, abort, Response, redirect, url_for
import pandas as pd
from hearthstone import deckstrings
from hearthstone.deckstrings import Deck
from hearthstone.enums import FormatType
import random
import os
import time
import hearthhome

app = Flask(__name__)

#The home page
@app.route('/')
def index():
        return render_template('index.html')
#Whenever the button is pressed the deckcode is posted to the website
@app.route("/yoggcode/", methods=['POST'])
def move_forward():
    return render_template('index.html', value=hearthhome.yogg_mage())

@app.route("/bigdruidcode/", methods=['POST'])
def move_forward2():
    return render_template('index.html', value2=hearthhome.big_druid())
#Sets the IP address to the address of the machine
if __name__ == "__main__":
        app.run(host='0.0.0.0', debug=True)
