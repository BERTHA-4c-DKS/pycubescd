import sys

sys.path.append("./modules")
import load_cube

filename = ""

if (len(sys.argv)) != 2:
    print "Usage: ", sys.argv[0], " filename.cube "
    exit(1)
else:
    filename = sys.argv[1]

cube = load_cube.cube(filename)

print "Number of points: " , \
        (cube.get_nx()*cube.get_ny()*cube.get_nz())
print "Total volume: ", cube.get_volume()

data = cube.mask_sphere (10.0, 0.0, 0.0, 0.0)

scube = cube 

scube.set_data(data)

of = open("out.cube", 'w+')
scube.dump(of)

