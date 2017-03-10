import sys
import numpy

import matplotlib.pyplot as plt

sys.path.append("./modules")
import load_cube

filenamea = ""
filenameb = ""
ax = ""

if (len(sys.argv)) != 4:
    print "Usage: ", sys.argv[0], " fileA.cube fileB.cube axis"
    exit(1)
else:
    filenamea = sys.argv[1]
    filenameb = sys.argv[2]
    ax = sys.argv[3]

cubeA = load_cube.cube(filenamea)
cubeB = load_cube.cube(filenameb)

cube = cubeA - cubeB

v = cube.cd(ax) 
vals = numpy.array(v)

plt.clf()
plt.plot(vals[:,0], vals[:,1], 'red', linestyle='--', linewidth=2, label='CD')
plt.plot(vals[:,0], vals[:,2], 'blue', linestyle='--', linewidth=2, label='VALUES')
legend = plt.legend(loc='upper right', shadow=True, fontsize='small')

plt.xlabel('X')
plt.ylabel('Y')
plt.show()

