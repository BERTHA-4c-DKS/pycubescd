import sys
import numpy

import matplotlib.pyplot as plt

sys.path.append("./modules")
import load_cube

filenamea = ""
filenameb = ""

if (len(sys.argv)) != 3:
    print "Usage: ", sys.argv[0], " fileAB.cube fileA.cube fileB.cube"
    exit(1)
else:
    filenamea = sys.argv[1]
    filenameb = sys.argv[2]

cubeA = load_cube.cube(filenamea)
cubeB = load_cube.cube(filenameb)

cube = cubeA - cubeB

#print cube

ymin = cube.get_origin()[1]
dy = cube.get_dy()
#vals = cube.integrate("z") # z 
vals = cube.integrate("y") # y
#vals = cube.integrate("x") # x 
i = 0
xv = []
cd = []
vl = []
for v in vals:
    xv.append(ymin+i*dy) 
    cd.append(numpy.sum( vals[:i] ) * dy)
    vl.append(v)
    i = i + 1

plt.clf()
plt.plot(xv, cd, 'red', linestyle='--', linewidth=2, label='CD')
plt.plot(xv, vl, 'blue', linestyle='--', linewidth=2, label='VALUES')
legend = plt.legend(loc='upper right', shadow=True, fontsize='small')

plt.xlabel('X')
plt.ylabel('Y')
plt.show()

