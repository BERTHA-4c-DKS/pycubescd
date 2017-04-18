import matplotlib.pyplot as plt
import numpy as np 
import argparse

import sys

sys.path.append("./modules")
import load_cube

parser = argparse.ArgumentParser()
parser.add_argument("-ftot","--filetot", help="cube format file to perform CD", \
        required=True, type=str)
parser.add_argument("-f1","--filefrag1", help="cube format file to perform CD", \
        required=True, type=str)
parser.add_argument("-f2","--filefrag2", help="cube format file to perform CD", \
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

print('Reading...' + args.filetot)

if not (os.path.isfile(args.filetot)):
    print "File ", args.filetot, " does not exist "
    exit(1)

totcube = load_cube.cube()
totcube.readfile(args.filetot)

print('Reading...' + args.filefrag1)

if not (os.path.isfile(args.filefrag1)):
    print "File ", args.filefrag1, " does not exist "
    exit(1)

frag1cube = load_cube.cube()
frag1cube.readfile(args.filefrag1)

print('Reading...' + args.filefrag2)

if not (os.path.isfile(args.filefrag2)):
    print "File ", args.filefrag2, " does not exist "
    exit(1)

frag2cube = load_cube.cube()
frag2cube.readfile(args.filefrag2)

if args.verbose:
    print "Performing the cube operation totcube - frag1cube - frag2cube"

mycube = totcube - frag1cube - frag2cube
outfilename = 'cd"+args.axis+".out'

if os.path.exists(outfilename):
    print "File ", outfilename, " exist, removing it "
    os.remove(outfilename)

cddata = mycube.cdx(outfilename)

print(type(args.isodensitypoint))

x = np.transpose(np.array(cddata))[0]
y = np.transpose(np.array(cddata))[1]

if args.isodensitypoint is not None:
   isovalue = args.isodensitypoint  
   from scipy.interpolate import interp1d
   dq_interpolated = interp1d(x, y, kind = 'cubic')
   ct = dq_interpolated(isovalue)
   print(isovalue,ct)
   dq_interpolated = interp1d(x, y, kind = 'linear')
   ct = dq_interpolated(isovalue)
   plt.plot(isovalue,ct)
   print(isovalue,ct)
   text = '('+str(isovalue)+',' + str(ct) + ')'
   plt.annotate(text, xy=(isovalue,ct), xytext=(isovalue+3.,ct), arrowprops=dict(facecolor='black', shrink=0.05))
   
plt.plot(x,y)

outfilename = 'cd"+args.axis+".eps'

if os.path.exists(outfilename):
    print "File ", outfilename, " exist, removing it "
    os.remove(outfilename)

print "Dumping file ", outfilename
plt.savefig(outfilename)
#plt.show()

integral=mycube.integrate()

print(integral)
