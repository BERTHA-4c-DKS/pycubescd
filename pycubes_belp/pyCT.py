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
parser.add_argument("-f","--file", help="3 cube format files: tot frag1 frag2", type=str, nargs=3)
parser.add_argument("--verbosity", help="increase output verbosity",action="store_true")
args = parser.parse_args()
#print(args.file)
#parser.print_help()
#print(len(args.addcubes))

if args.verbosity:
   print("verbosity turned on")  


print('Reading...' + args.file[0])
totcube = cubes.cube()
totcube.read(args.file[0])

print('Reading...' + args.file[1])
frag1cube = cubes.cube()
frag1cube.read(args.file[1])

print('Reading...' + args.file[2])
frag2cube = cubes.cube()
frag2cube.read(args.file[2])

print('Coping temp data...')
tmpdata = copy.copy(totcube.data)

dv = totcube.step_1[0]*totcube.step_2[1]*totcube.step_3[2]

partsum = 0.
for i in range(len(totcube.data)) :
      if (frag1cube.data[i] > frag2cube.data[i]):    
         partsum += totcube.data[i]

print('Electronic Charge on frag1', partsum*dv)

partsum = 0.
for i in range(len(totcube.data)) :
      if (frag1cube.data[i] < frag2cube.data[i]):    
         partsum += totcube.data[i]

print('Electronic Charge on frag2', partsum*dv)

print('Expected error due to cube sampling', totcube.integrate())



sys.exit()

