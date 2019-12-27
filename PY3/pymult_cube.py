import argparse
import sys

import os.path

sys.path.append("./modules")
import load_cube

parser = argparse.ArgumentParser()
parser.add_argument("-f1","--file1", help="cube format file to be multiplied", type=str)
parser.add_argument("-f2","--file2", help="cube format file to be multiplied", type=str)
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
    print("File ", args.file1, " does not exist ")
    exit(1)

if not (os.path.isfile(args.file2)):
    print("File ", args.file2, " does not exist ")
    exit(1)


print(('Reading ' + args.file1))
mycube1 = load_cube.cube()
mycube1.readfile (args.file1)


print(('Reading ' + args.file2))
mycube2 = load_cube.cube()
mycube2.readfile (args.file2)

risu = mycube1 * mycube2

f = open(args.output_cubefile,"w")
risu.dump( f)
f.close()
