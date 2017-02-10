import matplotlib.pyplot as plt
import numpy as np 
import cubes 
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-ftot","--filetot", help="cube format file to perform CD", type=str)
parser.add_argument("-f1","--filefrag1", help="cube format file to perform CD", type=str)
parser.add_argument("-f2","--filefrag2", help="cube format file to perform CD", type=str)
parser.add_argument("-axis", help="Specify the axis on which evaluating CD. Choose among [X,Y,Z]", type=str, default="Z")
parser.add_argument("-iso","--isodensitypoint", help="This is a float determining the isodensty point along a chosen axis. An interpolation procedure is used.", type=float)
parser.add_argument("--verbosity", help="increase output verbosity",action="store_true")
args = parser.parse_args()
#print(args.file)
#parser.print_help()
#print(len(args.addcubes))

if args.verbosity:
   print("verbosity turned on")  

if (args.axis != 'Z' and args.axis != 'Y' and args.axis != 'X'):
   args.axis = 'Z' 
   print('Problem with the axis definition, we set it to the default Z value.')

print('Reading...' + args.filetot)
totcube = cubes.cube()
totcube.read(args.filetot)

print('Reading...' + args.filefrag1)
frag1cube = cubes.cube()
frag1cube.read(args.filefrag1)

print('Reading...' + args.filefrag2)
frag2cube = cubes.cube()
frag2cube.read(args.filefrag2)

mycube = totcube - frag1cube - frag2cube


if   (args.axis == 'X'):
     cddata = mycube.cdx('cdx.out')

elif (args.axis == 'Y'):
     cddata = mycube.cdy('cdy.out')

elif (args.axis == 'Z'):
     cddata = mycube.cdz('cdz.out')

print(type(args.isodensitypoint))

x = np.transpose(np.array(cddata))[0]
y = np.transpose(np.array(cddata))[1]


if args.isodensitypoint is not None:
   isovalue = args.isodensitypoint  
   from scipy.interpolate import interp1d

   dq_interpolated = interp1d(x, y, kind = 'cubic')
   ct             = dq_interpolated(isovalue)
   print(isovalue,ct)
   dq_interpolated = interp1d(x, y, kind = 'linear')
   ct             = dq_interpolated(isovalue)
   plt.plot(isovalue,ct)
   print(isovalue,ct)
   text = '('+str(isovalue)+',' + str(ct) + ')'
   plt.annotate(text, xy=(isovalue,ct), xytext=(isovalue+3.,ct), arrowprops=dict(facecolor='black', shrink=0.05))
   
plt.plot(x,y)
plt.show()

#for i in pts.tolist():
#         print(('%e %e %e %e') % (i[0], i[1], i[2], my_interpolating_function(np.array(i))))
integral=mycube.integrate()

print(integral)

exit()

import matplotlib.pyplot as plt
import numpy as np 
import cubes 
import argparse
from scipy.interpolate import RegularGridInterpolator
from scipy.interpolate import interp1d
from scipy.optimize import newton
from scipy.optimize import fmin 


parser = argparse.ArgumentParser()
parser.add_argument("-f1",   "--filefrag1", help="cube format file of molecular fragment 1", type=str, required=True)
parser.add_argument("-f2",   "--filefrag2", help="cube format file of molecular fragment 2", type=str, required=True)
parser.add_argument("-o_iso","--outputiso",  help="Output file name", type=str, default="stdout")
parser.add_argument("-axis", help="Specify the axis on which evaluating the isodensity value [X,Y,Z]", type=str, default="Z")
parser.add_argument("--verbosity", help="increase output verbosity",action="store_true")
args = parser.parse_args()
#print(args.file)
#parser.print_help()
#print(len(args.addcubes))

if args.verbosity:
   print("verbosity turned on")  

if (args.axis != 'Z' and args.axis != 'Y' and args.axis != 'X'):
   args.axis = 'Z' 
   print('Problem with the axis definition, we set it to the default Z value.')

print('Reading...' + args.filefrag1)
mycube = cubes.cube()
mycube.read(args.filefrag1)
x,y,z = np.array(mycube.get_grid_xyz())

data = np.reshape(mycube.data,(mycube.n_1,mycube.n_2,mycube.n_3),order='C')

# This is for fixing the range of sampling point (info arises from the cube grid)
nump = 1000   # Fix number of sampling points

if (args.axis == 'Z'):

     xpt1 = np.zeros(nump)
     xpt2 = np.zeros(nump)
     xpt3 = np.linspace(np.min(z),np.max(z),nump)
     xpt  = xpt3

elif (args.axis == 'Y'):

     xpt1 = np.zeros(nump)
     xpt2 = np.linspace(np.min(y),np.max(y),nump) 
     xpt3 = np.zeros(nump)
     xpt  = xpt2

elif (args.axis == 'X'):
             
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

print('Reading...' + args.filefrag2)
mycube = cubes.cube()
mycube.read(args.filefrag2)
x,y,z = np.array(mycube.get_grid_xyz())
data = np.reshape(mycube.data,(mycube.n_1,mycube.n_2,mycube.n_3),order='C')

print('Interpolating...' + args.filefrag2)
my_interpolating_function = RegularGridInterpolator((x,y,z),data, method ='linear')
y2 = my_interpolating_function(pts)


print('Interpol 1D..linear.')
ydiff = y2 - y1
fdiff = interp1d(xpt, ydiff, kind = 'linear')
try:
    isodensity_point = newton(fdiff,0.0)  #  find a root Note that your stating point should be close to the final result
    print('isodensity_point =',isodensity_point)
except ValueError :
      print('Oops problem in newton algorithm')

print('Interpol 1D..cubic.')
ydiff = (y2 - y1)**2
fdiff = interp1d(xpt, ydiff, kind = 'cubic')
isodensity_point = fmin(fdiff,[0.0])  #  find a root Note that your stating point should be close to the final result
print('isodensity_point =',isodensity_point)

#print(args.outputiso)

f = open(args.outputiso,'w')
f.write(('Isodensity point %e') % isodensity_point)
f.close()

integrate()

#plt.plot(xpt,ydiff)
#plt.plot(xpt3,fdiff(xpt3))
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





