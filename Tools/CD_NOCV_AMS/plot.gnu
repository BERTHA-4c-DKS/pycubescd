#!/bin/gnuplot
set terminal postscript color eps enhanced "Palatino" 12
set output "./all_cd.eps"
set encoding iso_8859_1 
#set xtics rotate by 25 offset -1,-2
set grid ytics lt 0 lw 1 lc rgb "#bbbbbb"
set grid xtics lt 0 lw 1 lc rgb "#bbbbbb"
set size 0.5,0.5
set lmargin 10
set bmargin 3.25
set rmargin 2
set tmargin 1
#set object 1 rectangle from screen 0,0 to screen 1,1 fillcolor rgb "white" behind
set xzeroaxis
set yzeroaxis

#set title "{/Times-Bold Charge Displacement functions}"

lw1=2
lw2=1
ps2=0.35
set style line 11 lt 1 lw lw1 pt 6 ps ps2 lc rgb "red"  # red
set style line 12 lt 1 lw lw1 pt 6 ps ps2 lc rgb "blue" # blue
set style line 13 lt 1 lw lw1 pt 6 ps ps2 lc rgb "#228B22" # forestgreen
set style line 14 lt 1 lw lw1 pt 6 ps ps2 lc rgb "#A0522D" # sienna
set style line 15 lt 1 lw lw2 pt 6 ps ps2 lc rgb "#FFA500" # orange
set style line 16 lt 1 lw lw2 pt 6 ps ps2 lc rgb "#FF6347" # tomato
set style line 21 lt 2 lw lw1 pt 6 ps ps2 lc rgb "red"  # red
set style line 22 lt 2 lw lw1 pt 6 ps ps2 lc rgb "blue" # blue
set style line 23 lt 2 lw lw1 pt 6 ps ps2 lc rgb "#228B22" # forestgreen
set style line 24 lt 2 lw lw1 pt 6 ps ps2 lc rgb "#A0522D" # sienna
set style line 25 lt 2 lw lw1 pt 6 ps ps2 lc rgb "#FFA500" # orange
set style line 26 lt 2 lw lw1 pt 6 ps ps2 lc rgb "#FF6347" # tomato

# ovverride
set style line 1 lt 2 lw lw1 pt 6 ps ps2  dt 3 lc rgb "black"
set style line 2 lt 1 lw lw1 pt 6 ps ps2 lc rgb "black"
set style line 11 lt 1 lw lw1 pt 6 ps ps2 lc rgb "red"
set style line 12 lt 1 lw lw1 pt 6 ps ps2 lc rgb "#228B22"
set style line 13 lt 1 lw lw1 pt 6 ps ps2 lc rgb "blue"
set style line 14 lt 1 lw lw1 pt 6 ps ps2 lc rgb "#4dbeee"
set style line 15 lt 1 lw lw1 pt 6 ps ps2 lc rgb "gray50"
set style line 16 lt 1 lw lw1 pt 6 ps ps2 lc rgb "gray70"
set style line 21 lt 1 lw lw1 pt 6 ps ps2 lc rgb "black"

set style line 99 lt 1.2 lw 1 lc rgb "#D8BFD8"
#set style line 99 lt 1.2 lw 1 lc rgb "#ff6666"
set xlabel "{/Palatino-Italic z}, \305"
set ylabel '{/Symbol D}q({/Palatino-Italic z}), e'

set xrange[-10:5]
set yrange[-0.4:0.2]

conv=0.5291772106

# a to be setted at the isovalue
a=-2.685742*conv

set arrow nohead nofilled  from a,-0.3 to a,0.2 lc rgb "black"

set key left
plot \
     'tot_diff_dens.cub_cdz.txt' u ($1*conv):2 w l ls 2 ti"{/Symbol Dr}^'_{tot}",\
     'nocv1.cub_cdz.txt' u ($1*conv):2 w l ls 11 lc rgb "red" smooth csplines ti"{/Symbol Dr}_1",\
     'nocv2.cub_cdz.txt' u ($1*conv):2 w l ls 12 lc rgb "blue" smooth csplines ti"{/Symbol Dr}_2",\
     'nocv3.cub_cdz.txt' u ($1*conv):2 w l ls 13 lc rgb "green" smooth csplines ti"{/Symbol Dr}_3",\
     'nocv4.cub_cdz.txt' u ($1*conv):2 w l ls 14 lc rgb "brown" smooth csplines ti"{/Symbol Dr}_4",\
     'nocv5.cub_cdz.txt' u ($1*conv):2 w l ls 15  ti"{/Symbol Dr}_5",\
     'nocv6.cub_cdz.txt' u ($1*conv):2 w l ls 16  ti"{/Symbol Dr}_6",\
     'nuclabels' u 1:2 with points ls 11 notitle,'nuclabels' u 1:($2+0.04):3 with labels notitle
