#!/usr/bin/env python2.7

import requests
import bs4
import urllib2
import pickle
import sys

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

    response = requests.get('http://www.miltonbrewery.co.uk/beers/%s.html'%beer_name)
    if response.status_code == 404: return "NO SITE FOUND"

    soup = bs4.BeautifulSoup(response.text)
    contents_tag = soup.select('#Content')
    return contents_tag[0].contents[3].string


beers = open("beers.txt")

lines = beers.readlines()

beers = {}

for line in lines:
    b_name, b_strength, b_cost_price, _ = line.split(',')
    b_desc = get_beer_desc(b_name.lower().strip())
    # b = Beer(b_name, b_strength, b_cost_price, b_desc)

    print "processing %s"%b_name

    beers[b_name.strip()] = {
        "name":b_name.strip(),
        "strength":float(b_strength),
        "cost_price":float(b_cost_price),
        "desc":str(b_desc)
        }

    # save img
    try:
        resp = urllib2.urlopen("http://www.miltonbrewery.co.uk/media/pumpclips/%s.png"
                               %b_name.lower().strip())
    except urllib2.URLError, e:
        if e.code == 404:
            try:
                resp = urllib2.urlopen("http://www.miltonbrewery.co.uk/media/pumpclips/%s.png"
                                       %b_name.strip().capitalize())
            except urllib2.URLError, e:
                sys.stderr.write('Cannot find image for beer: %s\n' % b_name)
                continue
        else:
            raise
    localFile = open('fig/%s.png' % b_name.strip().lower(), 'w')
    localFile.write(resp.read())
    localFile.close()


# beers = sorted(beers, key=lambda b: b['name'])

pickle.dump(beers, open("beers.pkl","wb"))
