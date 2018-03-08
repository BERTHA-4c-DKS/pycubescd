import matplotlib.pyplot as plt
import numpy as np 
import argparse
from scipy.interpolate import RegularGridInterpolator
from scipy.interpolate import interp1d
from scipy.optimize import newton
from scipy.optimize import fmin 

import os
import sys
import os.path

sys.path.append("./modules")
import load_cube

parser = argparse.ArgumentParser()
parser.add_argument("-f1",   "--filefrag1", help="cube format file", \
        type=str, required=True)
parser.add_argument("-axis", help="Specify the axis on which evaluating the cube data",\
        type=str, default="z")
parser.add_argument("-o","--outfile",  help="Output file name", \
        type=str, default="stdout")
parser.add_argument("--verbose", help="increase output verbosity", \
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

print('Reading...' + args.filefrag1)
mycube = load_cube.cube()

if not (os.path.isfile(args.filefrag1)):
    print "File ", args.filefrag1, " does not exist "
    exit(1)

mycube.readfile(args.filefrag1)
x, y, z = np.array(mycube.get_grid_xyz())

data = mycube.get_data()

# This is for fixing the range of sampling point (info arises from the cube grid)
nump = 10000   # Fix number of sampling points

if (args.axis == 'z'):

     xpt1 = np.zeros(nump)
     xpt2 = np.zeros(nump)
     xpt3 = np.linspace(np.min(z),np.max(z),nump)
     xpt  = xpt3

elif (args.axis == 'y'):

     xpt1 = np.zeros(nump)
     xpt2 = np.linspace(np.min(y),np.max(y),nump) 
     xpt3 = np.zeros(nump)
     xpt  = xpt2

elif (args.axis == 'x'):
             
     xpt1 = np.linspace(np.min(x),np.max(x),nump)
     xpt2 = np.zeros(nump)
     xpt3 = np.zeros(nump)
     xpt  = xpt1

print('info... of sampling (nump, args.axis)', nump, args.axis)

print('Interpolating...' + args.filefrag1)
my_interpolating_function = RegularGridInterpolator((x,y,z),data, method ='linear')
#my_interpolating_function = RegularGridInterpolator((x,y,z),data, method ='nearest') 

pts = np.transpose([xpt1,xpt2,xpt3])
y1 = my_interpolating_function(pts)

#plt.plot(xpt,ydiff)
plt.plot(xpt,y1)

#if os.path.exists(outfilename):
#    print "File ", outfilename, " exist, removing it "
#    os.remove(outfilename)
#
#print "Dumping file ", outfilename
#plt.savefig(outfilename)
#plt.show()

#zz = mycube.cdz('cdz.out')
#zz = mycube.cdy('cdy.out')
#zz = mycube.cdx('cdx.out')
#mycube.toXYZ()
#b.read_cube('drho1.cube')
#c = a 
#c.print_cube('test.cub')
#x = np.transpose(np.array(zz))[0]
#y = np.transpose(np.array(zz))[1]
#plt.plot(x,y)
#plt.show()

#xpt1 = np.zeros(10000)
#xpt2 = np.zeros(10000)
#xpt1 = np.full(10000,0.142727)
#xpt2 = np.full(10000,0.142727)
#xpt3 = np.linspace(-10,10,10000)
#pts = np.transpose([xpt1,xpt2,xpt3])
#my_interpolating_function(pts)
#for i in pts.tolist():
#         print(('%e %e %e %e') % (i[0], i[1], i[2], my_interpolating_function(np.array(i))))
#plt.plot(np.transpose(pts)[2],my_interpolating_function(pts))
#plt.show()
outfilename = args.outfile

if os.path.exists(outfilename):
      os.remove(outfilename)

print('writing...' + args.outfile)
f = open(outfilename,'w')
f.write("# X      Y     Z     DENS_VALUE \n") 
for i in pts.tolist():
        f.write(('%e %e %e %e \n') % (i[0], i[1], i[2], my_interpolating_function(np.array(i))))

f.close()

