import numpy as np 
import argparse
import copy 
import sys
import os

sys.path.append("./modules")
import load_cube


"""
Generalized the idea of the isodensity: spatial grid is assegned tyo fragment 1 or 2 
depending on their relative density value. 
Density based descriptors for the CT and polarization effects associated with the 
interaction between two fragments and the formation of the chemical bond are reported.
see "Advances in Charge Displacement Analysis" Bistoni, Belpassi, Taratelli JCTC, 12,1236-1244 (2016).
"""

parser = argparse.ArgumentParser()
parser.add_argument("-f","--file", help="1 cube format files: tot " \
        " filename separator is a space", required=True, type=str, nargs=1)
parser.add_argument("-v", "--verbose", help="increase output verbosity", default=False, \
        action="store_true")

args = parser.parse_args()

if args.verbose:
   print("verbosity turned on")  

if args.verbose:
  print(('Reading...' + args.file[0]))

if not (os.path.isfile(args.file[0])):
    print("File ", args.file[0], " does not exist ")
    exit(1)

totcube = load_cube.cube()
totcube.readfile(args.file[0])

dv = totcube.get_dx()*totcube.get_dy()*totcube.get_dz()

partsum = 0.
for i in range(len(totcube.get_rawdata())) :
      if ( totcube.get_rawdata()[i] > 0.0):    
         partsum += totcube.get_rawdata()[i]

partial_positive=partsum*dv

print(('Integration of positive displacement', partial_positive))

partsum = 0.
for i in range(len(totcube.get_rawdata())) :
      if (totcube.get_rawdata()[i] < 0.0):    
         partsum += totcube.get_rawdata()[i]
partial_negative=partsum*dv
print(('Integration of negative displacement', partial_negative))
