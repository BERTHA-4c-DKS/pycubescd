import matplotlib.pyplot as plt
import numpy as np 
import argparse
import sys

import os.path

from scipy.interpolate import interp1d

sys.path.append("./modules")
import load_cube

parser = argparse.ArgumentParser()
parser.add_argument("-f","--file", help="cube format file to perform CD", type=str)
parser.add_argument("--axis", help="Specify the axis on which evaluating CD. " \
        "Choose among [x,y,z]", required=False, type=str, default="z")
parser.add_argument("-i","--isodensitypoint", \
        help="This is a float determining the isodensty point along a chosen axis. "\
        "An interpolation procedure is used.", type=float)
parser.add_argument("-v", "--verbose", help="increase output verbosity", default=False, \
        action="store_true")
parser.add_argument("-o","--outfilename", help="text output filename", \
        required=False, type=str, default="out.txt")
parser.add_argument("-p","--plotoutfilename", help="EPS output filename", \
        required=False, type=str, default="cd.eps")


if len(sys.argv) == 1:
    parser.print_help()
    exit(1)

args = parser.parse_args()

if args.verbose:
    print("verbosity turned on")  

if (args.axis != 'z' and args.axis != 'y' and args.axis != 'x'):
    args.axis = 'z' 
    print('Problem with the axis definition, we set it to the default z value.')

if not (os.path.isfile(args.file)):
    print "File ", args.file, " does not exist "
    exit(1)

print('Reading ' + args.file)
mycube = load_cube.cube()
mycube.readfile (args.file)

outfilename = args.outfilename

if os.path.exists(outfilename):
    print "File ", outfilename, " exist, removing it "
    os.remove(outfilename)

print "Writing ... " + outfilename

if (args.axis == 'z'):
    cddata = mycube.cdz(outfilename)

if (args.axis == 'y'):
    cddata = mycube.cdy(outfilename)

if (args.axis == 'x'):
    cddata = mycube.cdx(outfilename)

#print(type(args.isodensitypoint))

x = np.transpose(np.array(cddata))[0]
y = np.transpose(np.array(cddata))[1]

if args.isodensitypoint is not None:

   isovalue = args.isodensitypoint  
   dq_interpolated = interp1d(x, y, kind = 'cubic')
   ct = dq_interpolated(isovalue)
   print(isovalue,ct)
   dq_interpolated = interp1d(x, y, kind = 'linear')
   ct = dq_interpolated(isovalue)
   plt.plot(isovalue, ct)
   print(isovalue, ct)
   text = '('+str(isovalue)+',' + str(ct) + ')'
   plt.annotate(text, xy=(isovalue,ct), xytext=(isovalue+3.,ct), \
           arrowprops=dict(facecolor='black', shrink=0.05))

   f = open('CT_iso.dat',"a")
   f.write("isovalue:%e  CT_iso:%e %s\n" % (isovalue, ct,args.file))
   f.close()
   
plt.plot(x,y)
#plt.show()
outfilename = args.plotoutfilename

if os.path.exists(outfilename):
    print "File ", outfilename, " exist, removing it "
    os.remove(outfilename)

print "Dumping file ", outfilename
plt.savefig(outfilename)

integral = mycube.integrate()

print (integral)
