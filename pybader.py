import sys
import numpy
import argparse

sys.path.append("./modules")
import load_cube

"""
Used to evaluate the partial integral of an integrand in cube format on
a Bader's volume mapped on cube.
A cube Bader's volume can be generated using program bader:
W. Tang, E. Sanville, and G. Henkelman A grid-based Bader analysis algorithm 
without lattice bias, J. Phys.: Condens. Matter 21, 084204 (2009). 
http://theory.cm.utexas.edu/henkelman/code/bader/
For instance I used: bader -p all_bader -vac 0.000000001 density.cube
This gives a cube of each bader's volume on which the density is mapped.
!! ATTENTION for realable results density.cube and integrand cube HAS TO BE CONFORM..... 
"""

parser = argparse.ArgumentParser()
parser.add_argument("-f","--file", help="cube format file to integrate", \
        required=True, type=str)
parser.add_argument("-fb","--filebader", help="bader volume", required=True, 
        type=str)
parser.add_argument("-v", "--verbose", help="increase output verbosity", default=False, \
        action="store_true")

if len(sys.argv) == 1:
    parser.print_help()
    exit(1)

args = parser.parse_args()

if args.verbose:
   print("verbose turned on")  

print('Reading...' + args.file)

if not (os.path.isfile(args.file)):
    print "File ", args.file, " does not exist "
    exit(1)

totcube = load_cube.cube()
totcube.readfile (args.file)

print('Reading...' + args.filebader)

if not (os.path.isfile(args.filebader)):
    print "File ", args.filebader, " does not exist "
    exit(1)

badercube = load_cube.cube()
badercube.readfile (args.filebader)

dv = totcube.get_dx() * totcube.get_dy() * totcube.get_dz()

s = 0.0
for i in range(totcube.get_nx()):
    for j in range(totcube.get_ny()):
        for k in range(totcube.get_nz()):
            if (badercube.get_data()[i,j,k] > 0.0000000001) :
                s += totcube.get_data()[i,j,k]

print (s*dv)
print (numpy.sum(totcube.get_data())*dv)

exit()
