# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from collections import OrderedDict
import os
import requests
import logging

BASE_URL="https://www.realtor.com"
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
}
logging.basicConfig(level=logging.INFO)


def parse_args():
    import argparse

    parser = argparse.ArgumentParser(description='Parse realtor.com page.')
    parser.add_argument('fpath', 
                    help='path of realtor.com page')

    return(parser.parse_args())

def parse_path(fpath):
    if os.path.isfile(fpath):
        if p:
           yield p
    elif os.path.isdir(fpath):
        for fname in os.listdir(fpath):
            f = os.path.join(fpath, fname)
            logging.debug(f)
            if not os.path.isfile(f):
                continue
            for p in parse_file(f):
                if p:
                    yield p


def parse_file(fpath):
    with open(fpath) as fp:
        soup = BeautifulSoup(fp, "lxml")
    proplist = soup.findAll("li", {"class": "component_property-card"})
    if not proplist:       
        parse = parse_property(soup)
        return [parse]
    return iter(parse_property_url(prop) for prop in proplist)


def parse_property_url(prop):
    try:
        prop_url = BASE_URL+prop["data-url"]
        page = requests.get(prop_url, headers=headers)
        soup = BeautifulSoup(page.content, "lxml")
        parse =  parse_property(soup)
        return parse
    except (KeyError, requests.exceptions.TooManyRedirects):
        return


def parse_property(soup):
    if not soup.find(id="full_address_display"):
       return
    d = OrderedDict()
    keys = ["full_address_display", "price", "rent", "home_insurance", "hoa_fees", "property_tax"]
    for k in keys:
        try:
            d[k] = soup.find(id=k)["value"]
        except TypeError:
            d[k] = "" 
    return (", ".join( d.values()))

if __name__=="__main__":
    args = parse_args()

    for p in parse_path(args.fpath):
        print(p)


