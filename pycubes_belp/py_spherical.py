import matplotlib.pyplot as plt
import numpy as np 
import cubes 
import argparse
import copy 

"""
Generalized the idea of the isodensity: spatial grid is assegned tyo fragment 1 or 2 
depending on their relative density value. 
"""

parser = argparse.ArgumentParser()
parser.add_argument("-f","--file", help="cube format file to perform CD", type=str)
parser.add_argument("--verbosity", help="increase output verbosity",action="store_true")
args = parser.parse_args()
#print(args.file)
#parser.print_help()
#print(len(args.addcubes))

if args.verbosity:
   print("verbosity turned on")  


print('Reading...' + args.file)
totcube = cubes.cube()
totcube.read(args.file)

center = [0.0,0.0,2.876163]
r = []
rint = []

for rr in [0., 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2., 2.2, 2.4, 2.6, 2.8, 3., 3.2,3.4,3.6,3.8,4.,5., 6.]:
    radius = float(rr) 
    integral =totcube.spherical_int(center,radius)
    r.append(radius)
    rint.append(integral)
    print(rr, integral)

sys.exit()

