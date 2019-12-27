import matplotlib.pyplot as plt
import numpy  
import argparse
import copy 
import os.path
import math

import sys
import decimal

sys.path.append("./modules")
import load_cube
import elements

###############################################################################

def frange(x, y, jump):
    while x < y:
        yield x
        x += jump

###############################################################################

"""
compute the spherical integral 
"""

parser = argparse.ArgumentParser()
parser.add_argument("-f","--file", help="cube format file to be used ", \
        required=True, type=str)
parser.add_argument("-c","--center", help="X,Y,Z coordinate of the center "\
        "(e.g. --center \" 0,0,0\" a space at the beginning may be needed)", \
        required=False, type=str, default="0.0,0.0,0.0")
parser.add_argument("-dr","--deltar", help="dR step value ", \
        required=True, type=str)
parser.add_argument("-ax","--axis", help="axis to use mx, x, my, y, mz or z ", \
        required=False, type=str, default="N")
parser.add_argument("-anx","--angle", help="angle to use with respect to axis selected", \
        required=False, type=str, default="180")
parser.add_argument("-p","--plotoutfilename", help="EPS output filename", \
        required=False, type=str, default="cd.eps")
parser.add_argument("-o","--outfilename", help="text output filename", \
        required=False, type=str, default="out.txt")

if len(sys.argv) == 1:
    parser.print_help()
    exit(1)

args = parser.parse_args()

dr = float(args.deltar)

if not (os.path.isfile(args.file)):
    print("File ", args.file, " does not exist ")
    exit(1)

print(('Reading... ' + args.file))
cube = load_cube.cube()
cube.readfile(args.file)
axis = args.axis
angle = float(args.angle)

center = [0.0, 0.0, 0.0]

cs = args.center 
scs = cs.split(",")

if len(scs) != 3:
    print("Error in center values")
    exit(1)

for i in range(len(scs)):
    center[i] = float(scs[i])
    #print center[i] 

rmax = cube.get_enclosed_r(center, axis) 

nstep = int(rmax/dr) - 1

if (nstep <= 0):
    print("Error invalid number of steps")
    exit(1)

print("R: ", rmax, " nstep: ", nstep)
print("Start computing ... ")

rv = cube.spherical_int_rdr(center, rmax, dr, axis, angle)

outfilename = args.outfilename

if os.path.exists(outfilename):
    print("File ", outfilename, " exist, removing it ")
    os.remove(outfilename)

print("Writing ... " + outfilename)

fp = open(outfilename, "w")

cd = []
r = 0.0
for i in range(0, len(rv)):
    #print r , numpy.sum( rv[:i] ) * dr, rv[i]
    fp.write(str(r) + " " + str(numpy.sum( rv[:i] ) ) \
            + " " + str(rv[i]) + "\n")
    #cd.append([r , numpy.sum( rv[:i] ) * 4.0 * math.pi * r**2 * dr, rv[i]])
    cd.append([r , numpy.sum( rv[:i] ), rv[i]])
    r = r + dr

fp.close()

v = numpy.array(cd)


plt.clf()
#fig = plt.figure()
#ax = fig.add_subplot(1, 1, 1)

plt.plot(v[:,0], v[:,1], 'red', linestyle='--', linewidth=2, label='CD')
plt.plot(v[:,0], v[:,2], 'blue', linestyle='--', linewidth=2, label='VALUES')
legend = plt.legend(loc='upper right', shadow=True, fontsize='small')

plt.xlabel('X')
plt.ylabel('Y')

font = {'family': 'serif', 'color':  'darkred', 'weight': 'normal', 'size': 16}
atoms = cube.get_atoms()

for a in atoms:
    coords = a.get_coordinates()

    dist = math.sqrt((center[0] - coords[0])**2 + \
            (center[1] - coords[1])**2 + \
            (center[2] - coords[2])**2)
    if a.get_Z() != 1:
        #print dist, a.get_Z()
        plt.text(dist, 0.0, elements.ztosymbol[a.get_Z()], fontdict=font)

outfilename = args.plotoutfilename

if os.path.exists(outfilename):
    print("File ", outfilename, " exist, removing it ")
    os.remove(outfilename)

print("Dumping file ", outfilename)
plt.savefig(outfilename)
#plt.show()
