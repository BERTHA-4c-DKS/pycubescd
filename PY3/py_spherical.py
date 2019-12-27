import matplotlib.pyplot as plt
import numpy as np 
import argparse
import copy 
import os.path

import sys
import decimal

sys.path.append("./modules")
import load_cube

def frange(x, y, jump):
    while x < y:
        yield x
        x += jump

"""
Generalized the idea of the isodensity: spatial grid is assegned tyo fragment 1 or 2 
depending on their relative density value. 
"""

parser = argparse.ArgumentParser()
parser.add_argument("-f","--file", help="cube format file to perform CD", \
        required=True, type=str)
parser.add_argument("--verbose", help="increase output verbosity", \
        default=False, action="store_true")

if len(sys.argv) == 1:
    parser.print_help()
    exit(1)

args = parser.parse_args()
#print(args.file)
#parser.print_help()
#print(len(args.addcubes))

if args.verbose:
   print("verbosity turned on")  

print(('Reading...' + args.file))
totcube = load_cube.cube()

if not (os.path.isfile(args.file)):
    print("File ", args.file, " does not exist ")
    exit(1)

totcube.readfile(args.file)

center = [0.0,0.0,2.876163]
r = []
rint = []
#print list(frange(0.0, 6.0, 0.2))

for rr in [0., 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2., \
        2.2, 2.4, 2.6, 2.8, 3., 3.2,3.4,3.6,3.8,4.,5., 6.]:
    radius = float(rr) 
    integral =totcube.spherical_int(center,radius)
    r.append(radius)
    rint.append(integral)
    print((rr, integral))
