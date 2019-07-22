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
parser.add_argument("-o","--outfilename", help="text output filename", \
        required=False, type=str, default="")


if len(sys.argv) == 1:
    parser.print_help()
    exit(1)

args = parser.parse_args()

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

dy = mycube.get_dy()

dx = mycube.get_dx()
dz = mycube.get_dz()

ystart = mycube.get_origin()[1]

xstart = mycube.get_origin()[0]
zstart = mycube.get_origin()[2]
ytor = 0.0

diff = int((ytor - mycube.get_origin()[1])/mycube.get_dy() + 0.5)
print diff, mycube.get_origin()[1] + (diff * mycube.get_dy())

data = mycube.get_data()

if os.path.exists(outfilename):
    print "File ", outfilename, " exist, removing it "
    os.remove(outfilename)

fp = open(outfilename, "wa")

x = xstart
for ix in range(data[:, diff, :].shape[0]):
    z = zstart
    for iz in range(data[:, diff, :].shape[1]):
        fp.write("%10.5f %10.5f %20.10f\n"%(x, z, data[ix, diff, iz]))

        z = z + dz
    x = x + dx


fp.close()

integral = mycube.integrate()

print "Integral value: ", integral
