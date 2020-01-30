# README #
# REQUIREMENTS#
You need python, matplotlib, scipy  (Under Ubuntu: sudo apt install python-matplotlib; sudo apt install python-scipy)

Need to set in your ~/.bashrc the DIRPYCUBESCD variable 
 
DIRPYCUBESCD=......../pycubescd [for example /home/diego/pycubescd]
export PYTHONPATH=$PYTHONPATH:$DIRPYCUBESCD:$DIRPYCUBESCD/modules


CD code and related cubes module
to compile it: python -m compileall pyCD.py 

pycd.py: Produce a CD curve using a single cube file

pybader.py: Used to evaluate the partial integral of an 
            integrand in cube format on a Bader's volume mapped 
            on cube.

pycdfrags.py: Produce a CD curve using three cubes the two fragments 
              and the total molecule

pycdexct.py: can be used for instance in the case of excited states 


pydt.py: Generalized the idea of the isodensity: spatial grid is assegned tyo fragment 1 or 2 
         depending on their relative density value. Density based descriptors for the CT and 
         polarization effects associated with the interaction between two fragments and the formation
         of the chemical bond are reported.

pydens_iso.py: 

py_spherical.py: Generalized the idea of the isodensity: spatial grid is assegned tyo 
                 fragment 1 or 2  depending on their relative density value. 

pyadd_cube.py : simple tool to add two cubes

pysub_cube.py : simple tool to subtract two cubes

py_central.py : integrate the difference using a sphere or a semi-sphere or even a 
                cone 

py_sphere.py : integrate a cube using a sphere or a semi-sphere or even a cone 
               similar to py_central.py but using a single cube 
