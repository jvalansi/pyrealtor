# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from collections import OrderedDict
import os


def parse_args():
    import argparse

    parser = argparse.ArgumentParser(description='Parse realtor.com page.')
    parser.add_argument('fpath', 
                    help='path of realtor.com page')

    return(parser.parse_args())

def parse_path(fpath):
    if os.path.isfile(fpath):
        yield parse_file(fpath)
    elif os.path.isdir(fpath):
        for root, dirs, files in os.walk(fpath, topdown=False):
            for f in files:
                if not f.endswith('realtor.com®.html'):
                    continue
                yield parse_file(os.path.join(root, f))

def parse_file(fpath):
    with open(fpath) as fp:
        soup = BeautifulSoup(fp, "lxml")
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


