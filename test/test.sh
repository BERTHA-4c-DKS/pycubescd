#!/bin/bash

# rho_a + rho_b = rho_a+b
python ../pyadd_cube.py  -f1 rho_a.cube -f2 rho_b.cube -o  rho_a+b.cube

# rho_ab - rho_a+b = drho
python  ../pysub_cube.py -f1 rho_ab.cube -f2 rho_a+b.cube -o drho.cube

# CD analysis on drho along z
python  ../pycd.py -f drho.cube -o drho.dsv

# plot results
gnuplot -persist << EOR
plot \
"correct_drho.dsv" u 1:3 w l lw 2 title "drho/dz (correct)", \
"correct_drho.dsv" u 1:2 w l lw 2 title "dq (correct)", \
"drho.dsv" u 1:3 w p lw 2 pt 8 title "drho/dz (yours)", \
"drho.dsv" u 1:2 w p lw 2 pt 8 title "dq (yours)"
EOR

# delete generated files
rm rho_a+b.cube drho.cube drho.dsv
