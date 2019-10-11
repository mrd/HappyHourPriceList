#!/usr/bin/env python2.7

import requests
import bs4
import urllib2
import pickle
import string
import sys
from unidecode import unidecode

# class Beer:

#     name = "none"
#     strength = 0.0
#     cost_price = 0.0
#     desc = "none"

#     def __init__(self, param_name, param_strength, param_cost_price, param_desc):
#         self.name = param_name
#         self.strength = float(param_strength)
#         self.cost_price = float(param_cost_price)
#         self.desc = param_desc


def get_beer_desc(beer_name):
    url = 'http://www.miltonbrewery.co.uk/beers/%s.html' % beer_name
    response = requests.get(url)
    if response.status_code == 404: return "NO SITE FOUND"

    soup = bs4.BeautifulSoup(response.text,"lxml")
    contents_tag = soup.select('#Content')
    text = unidecode(contents_tag[0].contents[3].string)
    return text


beers = open("beers.txt")

lines = beers.readlines()

beers = {}

for line in lines:
    b_brewery, b_name, b_strength, b_cost_price, b_donation = line.split(',')
    b_desc = get_beer_desc(b_name.replace(' ', '-').lower().strip())
    # b = Beer(b_name, b_strength, b_cost_price, b_desc)

    print "processing %s"%b_name.replace(' ', '-').lower().strip()

    beers[b_name.strip()] = {
        "brewery":b_brewery.strip(),
        "name":b_name.strip(),
        "strength":float(b_strength),
        "cost_price":float(b_cost_price),
        "desc":str(b_desc),
        "donation":float(b_donation)
        }

    # save img

    safe_name = b_name.replace(' ', '-').lower().strip()
    possible_names = [safe_name,
                      string.capitalize(safe_name),
                      string.capitalize(safe_name) + "_Web",
                      string.capitalize(safe_name) + "_web",
                      string.capitalize(safe_name) + "_Website",
                      string.capitalize(safe_name) + "webtransparent"]
    found_beer = False
    if b_brewery == 'Milton':
        for name in possible_names:
            try:
                url = "http://www.miltonbrewery.co.uk/media/pumpclips/%s.png" % name
                resp = urllib2.urlopen(url)
                localFile = open('fig/%s.png' % b_name.strip().lower(), 'w')
                localFile.write(resp.read())
                localFile.close()
                found_beer = True
            except urllib2.URLError, e:
                if e.code == 404:
                    continue
                else:
                    raise
        if not found_beer:
            sys.stderr.write('Cannot find image for beer: %s\n' % b_name)

# beers = sorted(beers, key=lambda b: b['name'])

pickle.dump(beers, open("beers.pkl","wb"))
