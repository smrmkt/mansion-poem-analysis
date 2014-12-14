#!/usr/bin/env python
#-*-coding:utf-8-*-

import argparse
from xml.etree.ElementTree import *

# args
parser = argparse.ArgumentParser()
parser.add_argument('in_path')
parser.add_argument('out_path')


if __name__ == '__main__':
    # setup
    args = parser.parse_args()
    in_path = args.in_path
    in_file = open(args.in_path, 'r').read()
    out_file = open(args.out_path, 'w')

    # parse
    tree = parse(in_file)
    elem = tree.getroot()
    print elem.tag