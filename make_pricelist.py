#! /usr/bin/env python2.7

import math
import pickle
import subprocess
import sys

beers = pickle.load(open("beers.pkl","r"))

data=open("happyhour_template.tex").read()

beer_name = sys.argv[1]
beer = beers[beer_name]

data = data.replace("<FIGNAME>", beer_name.lower())
data = data.replace("<NAME>", beer_name)
data = data.replace("<STRENGTH>", "%.1f"%beer['strength'])
data = data.replace("<COST_PRICE>", "%.2f"%beer['cost_price'])
donation = beer['donation'] or ((math.ceil(beer['cost_price']*1.2*10)/10.0) - beer['cost_price'])
data = data.replace("<DONATION>", "%d"%donation)
data = data.replace("<DESC>", beer['desc'])

text_file = open("happyhour_generated.tex", "w")
text_file.write(data)

# subprocess.call('pdflatex happyhour_generated.tex')
