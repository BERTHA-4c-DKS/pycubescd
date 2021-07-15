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
parser.add_argument("-f1",   "--filefrag1", help="cube format file of molecular fragment 1", \
        type=str, required=True)
parser.add_argument("-f2",   "--filefrag2", help="cube format file of molecular fragment 2", \
        type=str, required=True)
parser.add_argument("-iseed",   "--initialseed", help="initial seed (real numer). An estimated value of the isodensity value", \
        type=str, required=True)
parser.add_argument("-o_iso","--outputiso",  help="Output file name", \
        type=str, default="stdout")
parser.add_argument("-axis", help="Specify the axis on which evaluating the isodensity value [x,y,z]",\
        type=str, default="z")
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

print(('Reading...' + args.filefrag1))
mycube = load_cube.cube()

if not (os.path.isfile(args.filefrag1)):
    print("File ", args.filefrag1, " does not exist ")
    exit(1)

mycube.readfile(args.filefrag1)
x, y, z = np.array(mycube.get_grid_xyz(),dtype=object)

data = mycube.get_data()

print(('Interpolating...' + args.filefrag1))
my_interpolating_function1 = RegularGridInterpolator((x,y,z),data, method ='linear')

print(('Reading...' + args.filefrag2))
mycube = load_cube.cube()

if not (os.path.isfile(args.filefrag2)):
    print("File ", args.filefrag2, " does not exist ")
    exit(1)



mycube.readfile(args.filefrag2)
x2,y2,z2 = np.array(mycube.get_grid_xyz(),dtype=object)
data = mycube.get_data()

print(('Interpolating...' + args.filefrag2))
my_interpolating_function2 = RegularGridInterpolator((x2,y2,z2),data, method ='linear')




#print('min z...', np.min(z))
#print('max z...', np.max(z))
#print('min z2...', np.min(z2))
#print('max z2...', np.max(z2))
#print('max(min(z,z2)', np.max(np.array([np.min(z),np.min(z2)])))
#print('min(max(z,z2)', np.min(np.array([np.max(z),np.max(z2)])))

print('IMPORTANT...it is required that the intersection of two cubes is/= O ')
print('Explicit check is not done by the program ')
# TO DO

# This is for fixing the range of sampling point (info arises from the cube grid)
nump = 40000   # Fix number of sampling points

if (args.axis == 'z'):

    
     xmin = np.max(np.array([np.min(z),np.min(z2)])) 
     xmax = np.min(np.array([np.max(z),np.max(z2)]))

      

     xpt1 = np.zeros(nump)
     xpt2 = np.zeros(nump)
     xpt3 = np.linspace(xmin,xmax,nump)
     xpt  = xpt3

elif (args.axis == 'y'):

     xmin = np.max(np.array([np.min(y),np.min(y2)]))
     xmax = np.min(np.array([np.max(y),np.max(y2)]))


     xpt1 = np.zeros(nump)
     xpt2 = np.linspace(xmin,xmax,nump) 
     xpt3 = np.zeros(nump)
     xpt  = xpt2

elif (args.axis == 'x'):

     xmin = np.max(np.array([np.min(x),np.min(x2)]))
     xmax = np.min(np.array([np.max(x),np.max(x2)]))

             
     xpt1 = np.linspace(xmin,xmax,nump)
     xpt2 = np.zeros(nump)
     xpt3 = np.zeros(nump)
     xpt  = xpt1

print(('info... of sampling (nump, args.axis)', nump, args.axis))

pts = np.transpose([xpt1,xpt2,xpt3])

y1 = my_interpolating_function1(pts)
y2 = my_interpolating_function2(pts)


print('Interpol 1D..linear.')
ydiff = (y2 - y1)**4
fdiff = interp1d(xpt, ydiff, kind = 'linear')
try:
    isodensity_point = fmin(fdiff,args.initialseed)  #  find a root Note that your stating point should be close to the final result
    print("isodensity_point = ", isodensity_point[0])

except ValueError :
    print('Oops problem in newton algorithm')


if (args.axis == 'z'):
      isodensity_value = my_interpolating_function2([0.0,0.0,float(isodensity_point)])   
      print(('isodensity_value=',isodensity_value))

if (args.axis == 'y'):
      isodensity_value = my_interpolating_function1([0.0,float(isodensity_point),0.0])
      print(('isodensity_value=',isodensity_value))

if (args.axis == 'x'):
      isodensity_value = my_interpolating_function1([float(isodensity_point),0.0,0.0])
      print(('isodensity_value=',isodensity_value))



#print(args.outputiso)

if os.path.exists(args.outputiso):
    print("File ", args.outputiso, " exist, removing it ")
    os.remove(args.outputiso)

f = open(args.outputiso, 'w')
f.write(('Isodensity point at %f a.u. along axis %s Isodensity value of %f e/(a.u.)^3 \n') % (isodensity_point, args.axis, isodensity_value) )
f.close()

#plt.plot(xpt,ydiff)
plt.plot(xpt,y1)
plt.plot(xpt,y2)

text = 'isodensity point is' +str(isodensity_point)
plt.annotate(text, xy=(isodensity_point,0.005), xytext=(isodensity_point,0.005), \
        arrowprops=dict(facecolor='black', shrink=0.05))

text1 ='isodensity value is' +str(isodensity_value)
plt.annotate(text1, xy=(isodensity_point,0.005), xytext=(isodensity_point,0.05))

plt.ylim((-0.1,1.0))
plt.xlabel('r (a.u)')


outfilename = args.outputiso + ".eps"

if os.path.exists(outfilename):
    print("File ", outfilename, " exist, removing it ")
    os.remove(outfilename)

print("Dumping file ", outfilename)
plt.savefig(outfilename)
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
#print(np.transpose(pts)[2],my_interpolating_function(pts))
#plt.plot(np.transpose(pts)[2],my_interpolating_function(pts))
#plt.show()
