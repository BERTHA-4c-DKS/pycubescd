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
cube.get_grid_xyz()
print cube.spherical_int([0.0, 0.0, 0.0], 10.0)
cube.to_xyz()

exit(1)

#print cube

print cube.integrate()
vals = cube.integrate("x")
for v in vals:
    print v
#print cube.integrate("y")
#print cube.integrate("z")

print "Number of points: " , \
        (cube.get_nx()*cube.get_ny()*cube.get_nz())
print "Total volume: ", cube.get_volume()

data = cube.mask_sphere (10.0, 0.0, 0.0, 0.0)

scube = cube 

scube.set_data(data)

of = open("out.cube", 'w+')
scube.dump(of)

