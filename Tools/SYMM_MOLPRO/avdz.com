***,cf4
memory 400 m
gprint orbitals,civector
 
basis=avdz

!   COMPLEX 
 
symmetry X,Y
noorient
geometry = {angstrom;
2

be 0.00 0.00 0.00
ne 0.00 0.00 1.946
}
 
{hf;
wf,14,4,2;   ! qui definisco il tripletto, unica scelta!
occ,4,2,2,0;}

{multi;
occ,4,2,2,0;
closed,4,1,1,0;
wf,14,4,0;ORBITAL,2010.2;}

e_bene=energy

{cube,bene.cube,-1,100,100,100
density,2010.2
step,0.2,0.2,0.2
origin,0.0,0.0,0.0}

{matrop
load,Cnatfrag,ORB,2010.2,natural
OPRD,tmp11,Cnatfrag,1.1,1.1,2.0    !  contribution of orbital 1 of sym 1 to density matrix      
OPRD,tmp12,Cnatfrag,2.1,2.1,2.0    !  contribution of orbital 2 of sym 1 to density matrix
OPRD,tmp13,Cnatfrag,3.1,3.1,2.0    !  contribution of orbital 3 of sym 1 to density matrix
OPRD,tmp14,Cnatfrag,4.1,4.1,2.0    !  contribution of orbital 4 of sym 1 to density matrix
ADD,dens1,tmp11,tmp12,tmp13,tmp14

OPRD,tmp21,Cnatfrag,1.2,1.2,2.0    !  contribution of orbital 1 of sym 2 to density matrix
OPRD,tmp22,Cnatfrag,2.2,2.2,1.0    !  contribution of orbital 2 of sym 2 to density matrix occ 1
ADD,dens2,tmp21,tmp22

OPRD,tmp31,Cnatfrag,1.3,1.3,2.0    !  contribution of orbital 1 of sym 2 to density matrix
OPRD,tmp32,Cnatfrag,2.3,2.3,1.0    !  contribution of orbital 2 of sym 2 to density matrix occ 1
ADD,dens3,tmp31,tmp32

save,dens1,2011.2
save,dens2,2012.2
save,dens3,2013.2}


{cube,bene1.cube,-1,100,100,100
density,2011.2
step,0.2,0.2,0.2
origin,0.0,0.0,0.0}

{cube,bene2.cube,-1,100,100,100
density,2012.2
step,0.2,0.2,0.2
origin,0.0,0.0,0.0}

{cube,bene3.cube,-1,100,100,100
density,2013.2
step,0.2,0.2,0.2
origin,0.0,0.0,0.0}




!    FRAG1

symmetry X,Y
noorient
geometry = {angstrom;
1

be 0.00 0.00 0.00
}

{hf;
wf,4,1,0;
occ,1,1,0,0;}

{multi;
occ,1,1,1,0;
closed,0,0,0,0;
wf,4,4,0;ORBITAL,2020.2;}

e_be=energy

{cube,be.cube,-1,100,100,100
density,2020.2
step,0.2,0.2,0.2
origin,0.0,0.0,0.0}

{matrop
load,Cnatfrag,ORB,2020.2,natural
OPRD,dens1,Cnatfrag,1.1,1.1,2.0    !  contribution of orbital 1 of sym 1 to density matrix
OPRD,dens2,Cnatfrag,1.2,1.2,1.0    !  contribution of orbital 1 of sym 2 to density matrix
OPRD,dens3,Cnatfrag,1.3,1.3,1.0    !  contribution of orbital 1 of sym 3 to density matrix
save,dens1,2021.2
save,dens2,2022.2
save,dens3,2023.2}


{cube,be1.cube,-1,100,100,100
density,2021.2
step,0.2,0.2,0.2
origin,0.0,0.0,0.0}

{cube,be2.cube,-1,100,100,100
density,2022.2
step,0.2,0.2,0.2
origin,0.0,0.0,0.0}

{cube,be3.cube,-1,100,100,100
density,2023.2
step,0.2,0.2,0.2
origin,0.0,0.0,0.0}


!    FRAG2

symmetry X,Y
noorient
geometry = {angstrom;
1

ne 0.00 0.00 1.946
}

{hf;
wf,10,1,0;}

{multi;
occ,3,1,1,0;
closed,0,0,0,0;
wf,10,1,0;ORBITAL,2030.2;}

e_ne=energy

{cube,ne.cube,-1,100,100,100
density,2030.2
step,0.2,0.2,0.2
origin,0.0,0.0,0.0}


{matrop
load,Cnatfrag,ORB,2030.2,natural
OPRD,tmp11,Cnatfrag,1.1,1.1,2.0    !  contribution of orbital 1 of sym 1 to density matrix
OPRD,tmp12,Cnatfrag,2.1,2.1,2.0    !  contribution of orbital 1 of sym 1 to density matrix
OPRD,tmp13,Cnatfrag,3.1,3.1,2.0    !  contribution of orbital 1 of sym 1 to density matrix
ADD,dens1,tmp11,tmp12,tmp13

OPRD,dens2,Cnatfrag,1.2,1.2,2.0

OPRD,dens3,Cnatfrag,1.3,1.3,2.0

save,dens1,2031.2
save,dens2,2032.2
save,dens3,2033.2}

{cube,ne1.cube,-1,100,100,100
density,2031.2
step,0.2,0.2,0.2
origin,0.0,0.0,0.0}

{cube,ne2.cube,-1,100,100,100
density,2032.2
step,0.2,0.2,0.2
origin,0.0,0.0,0.0}

{cube,ne3.cube,-1,100,100,100
density,2033.2
step,0.2,0.2,0.2
origin,0.0,0.0,0.0}

ee = (e_bene - e_be - e_ne)*627.50954

table,e_bene, e_be, e_ne, ee

  
 -----
