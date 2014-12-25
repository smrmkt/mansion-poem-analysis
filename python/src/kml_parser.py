#!/usr/bin/env python
#-*-coding:utf-8-*-

import argparse
from xml.etree.ElementTree import *
import re

# args
parser = argparse.ArgumentParser()
parser.add_argument('in_path')
parser.add_argument('out_path')

def wrap(tag):
    return "{http://www.opengis.net/kml/2.2}"+tag

def get_title(e):
    name = e.find(".//{}".format(wrap("name"))).text
    r = re.compile("(\d+)\. (.*)")
    m = r.match(name)
    return m.group(1), m.group(2) #m.group(2)

def get_geo(e):
    geo = e.find(".//{}".format(wrap("coordinates"))).text.split(",")
    return geo[0], geo[1]

def get_price(e):
    lines = e.find(".//{}".format(wrap("description"))).text.split("\n")
    price_l, price_h = "", ""
    for line in lines:
        if line.find(u"万円") > -1:
            prices = line.split(u"～")
            prices = [price.replace(u"台", "") for price in prices]
            prices = [price.replace(u"(1戸)", "") for price in prices]
            prices = [price.replace(u" ", "") for price in prices]
            prices = [re.sub(r"[,]", "", price) for price in prices]
            prices = [re.sub(r"\D.*", "", price) for price in prices]
            if len(prices) == 2:
                price_l, price_h = prices
    return price_l, price_h

def get_description(e):
    desc = e.find(".//{}".format(wrap("description"))).text
    return desc.replace("\n", " ")

if __name__ == '__main__':
    # setup
    args = parser.parse_args()
    in_path = args.in_path
    out_file = open(args.out_path, 'w')

    # parse
    tree = parse(args.in_path)
    elem = tree.getroot()
    for e in elem.findall(".//{}".format(wrap("Placemark"))):
        no, title = get_title(e)
        longitude, latitude = get_geo(e)
        price_l, price_h = get_price(e)
        name, space_l, space_h, price_sm, developer, created = "", "", "", "", "", ""
        description = get_description(e)
        line = [no,
                name,
                longitude,
                latitude,
                price_l,
                price_h,
                price_sm,
                space_l,
                space_h,
                developer,
                created]
        out_file.write("\t".join(line))
        out_file.write("\t"+str(title.encode("utf-8")))
        out_file.write("\t"+str(description.encode("utf-8"))+"\n")
    out_file.close()

