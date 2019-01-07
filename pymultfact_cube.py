import argparse
import sys

import os.path

sys.path.append("./modules")
import load_cube

parser = argparse.ArgumentParser()
parser.add_argument("-f1","--file1", help="cube format file to be multiplied", type=str)
parser.add_argument("-factor", help="real number to scale", type=float, default = 1.000)
parser.add_argument("-o","--output_cubefile", help="result cube format file ", type=str)
parser.add_argument("-v", "--verbose", help="increase output verbosity", default=False, \
        action="store_true")

if len(sys.argv) == 1:
    parser.print_help()
    exit(1)

args = parser.parse_args()

if args.verbose:
    print("verbosity turned on")  

if not (os.path.isfile(args.file1)):
    print "File ", args.file1, " does not exist "
    exit(1)

factor = args.factor
print('Scale factort', factor)
print('Reading ' + args.file1)
mycube1 = load_cube.cube()
mycube1.readfile (args.file1)


risu = mycube1 
aa = risu.get_data() * factor 
risu.set_data(aa)

f = open(args.output_cubefile,"w")
risu.dump( f)
f.close()
