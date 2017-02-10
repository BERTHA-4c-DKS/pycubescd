import cubes 
import argparse

"""
Used to evaluate the partial integral of an integrand in cube format on
a Bader's volume mapped on cube.
A cube Bader's volume can be generated using program bader:
W. Tang, E. Sanville, and G. Henkelman A grid-based Bader analysis algorithm without lattice bias, J. Phys.: Condens. Matter 21, 084204 (2009). 
http://theory.cm.utexas.edu/henkelman/code/bader/
For instance I used: bader -p all_bader -vac 0.000000001 density.cube
This gives a cube of each bader's volume on which the density is mapped.
!! ATTENTION for realable results density.cube and integrand cube HAS TO BE CONFORM..... 
"""

parser = argparse.ArgumentParser()
parser.add_argument("-f","--file", help="cube format file to integrate", type=str)
parser.add_argument("-fb","--filebader", help="bader volume", type=str)
parser.add_argument("--verbosity", help="increase output verbosity",action="store_true")
args = parser.parse_args()

if args.verbosity:
   print("verbosity turned on")  


print('Reading...' + args.file)
totcube = cubes.cube()
totcube.read(args.file)

print('Reading...' + args.filebader)
badercube = cubes.cube()
badercube.read(args.filebader)



dv = totcube.step_1[0]*totcube.step_2[1]*totcube.step_3[2]

s = 0.
for i in range(len(totcube.data)) :
    if (badercube.data[i] > 0.0000000001) :
       s += totcube.data[i]

print(s*dv)
print(sum(totcube.data)*dv)

exit()
