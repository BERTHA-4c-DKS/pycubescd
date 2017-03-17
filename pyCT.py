import matplotlib.pyplot as plt
import numpy as np 
import argparse
import copy 
import sys

sys.path.append("./modules")
import load_cube


"""
Generalized the idea of the isodensity: spatial grid is assegned tyo fragment 1 or 2 
depending on their relative density value. 
"""

parser = argparse.ArgumentParser()
parser.add_argument("-f","--file", help="3 cube format files: tot frag1 frag2", type=str, nargs=3)
parser.add_argument("--verbosity", help="increase output verbosity",action="store_true")

if len(sys.argv) == 1:
    parser.print_help()
    exit(1)

args = parser.parse_args()

if args.verbosity:
   print("verbosity turned on")  

print('Reading...' + args.file[0])
totcube = load_cube.cube()
totcube.readfile(args.file[0])

print('Reading...' + args.file[1])
frag1cube = load_cube.cube()
frag1cube.readfile(args.file[1])

print('Reading...' + args.file[2])
frag2cube = load_cube.cube()
frag2cube.readfile(args.file[2])

print('Coping temp data...')

dv = totcube.get_dx()*totcube.get_dy()*totcube.get_dz()

partsum = 0.
for i in range(len(totcube.get_rawdata())) :
      if (frag1cube.get_rawdata()[i] > frag2cube.get_rawdata()[i]):    
         partsum += totcube.get_rawdata()[i]

print('Electronic Charge on frag1', partsum*dv)

partsum = 0.
for i in range(len(totcube.get_rawdata())) :
      if (frag1cube.get_rawdata()[i] < frag2cube.get_rawdata()[i]):    
         partsum += totcube.get_rawdata()[i]

print('Electronic Charge on frag2', partsum*dv)

print('Expected error due to cube sampling', totcube.integrate())

sys.exit()
