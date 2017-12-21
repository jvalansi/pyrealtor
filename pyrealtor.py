# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
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
                print(f)
                yield parse_file(os.path.join(root, f))

def parse_file(fpath):
    with open(fpath) as fp:
        soup = BeautifulSoup(fp, "lxml")
    d = {"home_insurance": None, "hoa_fees": None, "property_tax": None}
    for k in d:
        try:
            d[k] = soup.find(id=k)["value"]
        except TypeError:
            continue 
    return ("\t".join(filter(None, d.values())))

if __name__=="__main__":
    args = parse_args()
    
    for p in parse_path(args.fpath):
        print(p)


