import matplotlib.pyplot as plt
import numpy as np 
import argparse
import sys

sys.path.append("./modules")
import load_cube

parser = argparse.ArgumentParser()
parser.add_argument("-f","--file", help="cube format file to perform CD", type=str)
parser.add_argument("-axis", help="Specify the axis on which evaluating CD. Choose among [X,Y,Z]", type=str, default="Z")
parser.add_argument("-iso","--isodensitypoint", \
        help="This is a float determining the isodensty point along a chosen axis. "\
        "An interpolation procedure is used.", type=float)
parser.add_argument("--verbosity", help="increase output verbosity",action="store_true")

if len(sys.argv) == 1:
    parser.print_help()
    exit(1)

args = parser.parse_args()

if args.verbosity:
   print("verbosity turned on")  

if (args.axis != 'Z' and args.axis != 'Y' and args.axis != 'X'):
   args.axis = 'Z' 
   print('Problem with the axis definition, we set it to the default Z value.')

print('Reading...' + args.file)
mycube = load_cube.cube()
mycube.readfile (args.file)

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
