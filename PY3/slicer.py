import matplotlib.pyplot as plt
import numpy as np 
import argparse
import sys

import os.path

from scipy.interpolate import interp1d

sys.path.append("./modules")
import load_cube

parser = argparse.ArgumentParser()
parser.add_argument("-f","--file", help="cube format file to perform CD", required=True, 
        type=str)
parser.add_argument("-o","--outfilename", help="text output filename", \
        required=False, type=str, default="out.txt")
parser.add_argument("-p","--plane", help="plane to cut (default: xz)", \
        required=False, type=str, default="xz")
parser.add_argument("-v","--value", help="cut value (default: 0.0)", \
        required=False, type=float, default=0.0)

if len(sys.argv) == 1:
    parser.print_help()
    exit(1)

args = parser.parse_args()

if not (os.path.isfile(args.file)):
    print("File ", args.file, " does not exist ")
    exit(1)

print(('Reading ' + args.file))
mycube = load_cube.cube()
mycube.readfile (args.file)

outfilename = args.outfilename

if os.path.exists(outfilename):
    print("File ", outfilename, " exist, removing it ")
    os.remove(outfilename)

print("Writing ... " + outfilename)

dx = mycube.get_dx()
dy = mycube.get_dy()
dz = mycube.get_dz()

xstart = mycube.get_origin()[0]
ystart = mycube.get_origin()[1]
zstart = mycube.get_origin()[2]

data = mycube.get_data()

if os.path.exists(outfilename):
    print("File ", outfilename, " exist, removing it ")
    os.remove(outfilename)

fp = open(outfilename, "wa")

if args.plane == "xz":
    ycut = args.value
    diff = int((ycut - mycube.get_origin()[1])/mycube.get_dy() + 0.5)
    print(diff, mycube.get_origin()[1] + (diff * mycube.get_dy()))
    x = xstart
    for ix in range(data[:, diff, :].shape[0]):
        z = zstart
        for iz in range(data[:, diff, :].shape[1]):
            fp.write("%10.5f %10.5f %20.10f\n"%(x, z, data[ix, diff, iz]))
            z = z + dz
        x = x + dx
elif args.plane == "xy":
    zcut = args.value
    diff = int((zcut - mycube.get_origin()[2])/mycube.get_dz() + 0.5)
    print(diff, mycube.get_origin()[2] + (diff * mycube.get_dz()))
    x = xstart
    for ix in range(data[:,:, diff].shape[0]):
        y = ystart
        for iy in range(data[:, : , diff].shape[1]):
            fp.write("%10.5f %10.5f %20.10f\n"%(x, y, data[ix, iy, diff]))
            y = y + dy
        x = x + dx
elif args.plane == "yz":
    xcut = args.value
    diff = int((xcut - mycube.get_origin()[0])/mycube.get_dx() + 0.5)
    print(diff, mycube.get_origin()[0] + (diff * mycube.get_dx()))
    y = ystart
    for iy in range(data[diff, :, :].shape[0]):
        z = zstart
        for iz in range(data[diff, :, :].shape[1]):
            fp.write("%10.5f %10.5f %20.10f\n"%(y, z, data[diff, iy, iz]))
            z = z + dz
        y = y + dy

fp.close()

integral = mycube.integrate()

print("Integral value: ", integral)
