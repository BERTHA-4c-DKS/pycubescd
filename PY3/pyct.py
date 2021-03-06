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
parser.add_argument("-f","--file", help="3 cube format files: tot frag1 frag2 " \
        " filename separator is a space", required=True, type=str, nargs=3)
parser.add_argument("-v", "--verbose", help="increase output verbosity", default=False, \
        action="store_true")

if len(sys.argv) == 1:
    parser.print_help()
    exit(1)

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

if args.verbose:
  print(('Reading...' + args.file[1]))

if not (os.path.isfile(args.file[1])):
    print("File ", args.file[1], " does not exist ")
    exit(1)

frag1cube = load_cube.cube()
frag1cube.readfile(args.file[1])

if args.verbose:
  print(('Reading...' + args.file[2]))

if not (os.path.isfile(args.file[2])):
    print("File ", args.file[2], " does not exist ")
    exit(1)

frag2cube = load_cube.cube()
frag2cube.readfile(args.file[2])

if args.verbose:
  print('Coping temp data...')

dv = totcube.get_dx()*totcube.get_dy()*totcube.get_dz()

partsum = 0.
for i in range(len(totcube.get_rawdata())) :
      if (frag1cube.get_rawdata()[i] > frag2cube.get_rawdata()[i]):    
         partsum += totcube.get_rawdata()[i]

CTfrag1=partsum*dv

print(('Electronic Charge on frag1', CTfrag1))

partsum = 0.
for i in range(len(totcube.get_rawdata())) :
      if (frag1cube.get_rawdata()[i] < frag2cube.get_rawdata()[i]):    
         partsum += totcube.get_rawdata()[i]

CTfrag2=partsum*dv
print(('Electronic Charge on frag2', CTfrag2))
print(('Expected error due to cube sampling', totcube.integrate()))

partsum = 0.
for i in range(len(totcube.get_rawdata())) :
      if (totcube.get_rawdata()[i] < 0.0000):
            partsum += totcube.get_rawdata()[i]

Qtot = -partsum*dv

if (CTfrag1 < 0.00 ) :
     partsum = 0.
     for i in range(len(totcube.get_rawdata())) :
        if (totcube.get_rawdata()[i] > 0.0000):
            if (frag1cube.get_rawdata()[i] > frag2cube.get_rawdata()[i]):
               partsum += totcube.get_rawdata()[i]
     Qfrag1 = partsum*dv

     partsum = 0.
     for i in range(len(totcube.get_rawdata())) :
        if (totcube.get_rawdata()[i] < 0.0000):
            if (frag1cube.get_rawdata()[i] < frag2cube.get_rawdata()[i]):
               partsum += totcube.get_rawdata()[i]
     Qfrag2 = -partsum*dv

if (CTfrag1 > 0.00 ) :
     partsum = 0.
     for i in range(len(totcube.get_rawdata())) :
        if (totcube.get_rawdata()[i] < 0.0000):
            if (frag1cube.get_rawdata()[i] > frag2cube.get_rawdata()[i]):
               partsum += totcube.get_rawdata()[i]
     Qfrag1 = -partsum*dv

     partsum = 0.
     for i in range(len(totcube.get_rawdata())) :
        if (totcube.get_rawdata()[i] > 0.0000):
            if (frag1cube.get_rawdata()[i] < frag2cube.get_rawdata()[i]):
               partsum += totcube.get_rawdata()[i]
     Qfrag2 = partsum*dv


print('')
print(('Electronic Charge on frag1, CT = ', CTfrag1))
print('Note, a positive value means a charge accumulation in frag1')
print('')

f = open('CT_new.dat',"a")
f.write("CT: %f %s \n" % (CTfrag1,args.file))
f.close()


print('Density based descriptors for CT and polarization:details see JCTC,12, 1236 (2016)')
print('Qtot = Qfrag1+Qfrag2+|CT|')
print('')
print(("Qtot  = %f " % Qtot))
print(("Qfrag1= %f " % Qfrag1))
print(("Qfrag2= %f " % Qfrag2))
