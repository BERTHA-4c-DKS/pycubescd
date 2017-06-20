import matplotlib.pyplot as plt
import argparse
import numpy 
import os

import sys

sys.path.append("./modules")
import load_cube

parser = argparse.ArgumentParser()
parser.add_argument("-f1","--file1", help="cube format file to perform CD", \
        required=True, type=str)
parser.add_argument("-f2","--file2", help="cube format file to perform CD", \
        required=True, type=str)
parser.add_argument("-axis", help="Specify the axis on which evaluating CD. " \
        "Choose among [x,y,z]", type=str, default="z")
parser.add_argument("-iso","--isodensitypoint", 
        help="This is a float determining the isodensty point along a chosen axis. " \
                "An interpolation procedure is used.", type=float)
parser.add_argument("-v", "--verbose", help="increase output verbosity", \
        default=False, action="store_true")

if len(sys.argv) == 1:
    parser.print_help()
    exit(1)

args = parser.parse_args()

if args.verbose:
   print("verbosity turned on")  

if (args.axis != 'z' and args.axis != 'y' and args.axis != 'x'):
   args.axis = 'z' 
   print('Problem with the axis definition, we set it to the default z value.')

if not (os.path.isfile(args.file1)):
    print "File ", args.file1, " does not exist "
    exit(1)

cubeA = load_cube.cube(args.file1)

if not (os.path.isfile(args.file2)):
    print "File ", args.file2, " does not exist "
    exit(1)

cubeB = load_cube.cube(args.file2)

if args.verbose:
    print "Performing cubaA - cubeB"

cube = cubeA - cubeB

v = cube.cd(args.axis) 
vals = numpy.array(v)

plt.clf()
plt.plot(vals[:,0], vals[:,1], 'red', linestyle='--', linewidth=2, label='CD')
plt.plot(vals[:,0], vals[:,2], 'blue', linestyle='--', linewidth=2, label='VALUES')
legend = plt.legend(loc='upper right', shadow=True, fontsize='small')

plt.xlabel('X')
plt.ylabel('Y')

outfilename = "cd" + args.axis + ".eps"

if os.path.exists(outfilename):
    print "File ", outfilename, " exist, removing it "
    os.remove(outfilename)

print "Dumping file ", outfilename
plt.savefig(outfilename)
#plt.show()
