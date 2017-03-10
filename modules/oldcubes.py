import numpy as np 
import math
import copy 
import sys 

class cube(): 
     """
      Class to tract data in cube format
     """ 

     def __init__(self, natoms=0, origin=[0.,0.,0.],n_1=0,n_2=0,n_3=0,step_1=[0.,0.,0.], \
                  step_2=[0.,0.,0.],step_3=[0.,0.,0.],atoms=[0, 0.,0.,0.],data = []): 

         self.natoms = natoms 
         self.origin= origin 
         self.n_1= n_1
         self.n_2= n_2 
         self.n_3= n_3 
         self.step_1=step_1
         self.step_2=step_2
         self.step_3=step_3
         self.atoms = atoms
         self.data  = data 

     def clear(self):
         self.natoms = 0
         self.origin = [0.,0.,0.]
         self.n_1= 0
         self.n_2= 0
         self.n_3= 0 
         self.step_1= [0.,0.,0.] 
         self.step_2= [0.,0.,0.]
         self.step_3= [0.,0.,0.]
         self.atoms = [0, 0.,0.,0.]
         self.data  = []

     def get_natoms(self):
         return self.natoms

     def get_origin(self):
         return self.origin 

     def get_n_1(self):
         return self.n_1

     def get_n_2(self):
         return self.n_2

     def get_n_3(self):
         return self.n_3

     def get_step_1(self):
         return self.step_1

     def get_step_2(self):
         return self.step_2

     def get_step_3(self):
         return self.step_3

     def get_atoms(self):
         return self.atoms

     def get_data(self):
         return self.data

     def dump(self,fname):
         """Write cube in file 'fname' """

         f = open(fname,'w')
         f.write('This is a cube\n')         
         f.write('GENERATED \n')         
         f.write(('%5d %.6f %.6f %.6f \n') % (self.natoms, self.origin[0],self.origin[1],self.origin[2]))         
         f.write(('%5d %.6f %.6f %.6f \n') % (self.n_1,    self.step_1[0],self.step_1[1],self.step_1[2]))         
         f.write(('%5d %.6f %.6f %.6f \n') % (self.n_2,    self.step_2[0],self.step_2[1],self.step_2[2]))        
         f.write(('%5d %.6f %.6f %.6f \n') % (self.n_3,    self.step_3[0],self.step_3[1],self.step_3[2]))        
         for atom in self.atoms:
             f.write(('%d %s %s %s %s \n') % (atom[0], 0., atom[1],atom[2],atom[3]))

         count=0
         for data in self.data:
            f.write(('%.5e ') % (data))
            count +=1
            if (count % 6) == 0 :
               f.write('\n')
         f.close()
         
     def read(self,fname):
         try:
             f = open(fname,'r')

             line1 = f.readline().split()
             line2 = f.readline().split()

             line3 = f.readline().split()
             self.natoms = int(line3[0])
             self.origin = [float(line3[1]),float(line3[2]),float(line3[3])]

             line4 = f.readline().split()
             self.n_1    = int(line4[0])
             self.step_1 = [float(line4[1]),float(line4[2]),float(line4[3])]

             line5 = f.readline().split()
             self.n_2    = int(line5[0])
             self.step_2 = [float(line5[1]),float(line5[2]),float(line5[3])]

             line6 = f.readline().split()
             self.n_3    = int(line6[0])
             self.step_3 = [float(line6[1]),float(line6[2]),float(line6[3])]
             self.atoms = []

             for i in range(self.natoms):
                 nline = f.readline().split()
                 self.atoms.append([int(nline[0]),float(nline[2]),float(nline[3]),float(nline[4])])
 
             count = 0
             data = []
             for i in f :
                for v in i.split():
                    data.append(float(v)) 
             count += 1
             self.data = data
             f.close()  

         except:
             print(('Problem in opening/format of file %s ') % fname)
             sys.exit()
             raise
             

     def __add__(self,other):
         """Defines the '+' operator. Sum data of two cubes
            The header of resulting cube is of the left side cube 
         """

         aa = cube()
         aa.natoms = copy.copy(self.natoms)
         aa.origin = copy.copy(self.origin)
         aa.n_1    = copy.copy(self.n_1)
         aa.n_2    = copy.copy(self.n_2)
         aa.n_3    = copy.copy(self.n_3)
         aa.step_1 = copy.copy(self.step_1)
         aa.step_2 = copy.copy(self.step_2)
         aa.step_3 = copy.copy(self.step_3)
         aa.atoms  = copy.copy(self.atoms)
         aa.data   = np.array(self.data) + np.array(other.data)
         return aa

     def __sub__(self,other):
         """ Defines the '-' operator. Difference of data of two cubes
             The header of resulting cube is of the left side cube
         """

         aa = cube()
         aa.natoms = copy.copy(self.natoms)
         aa.origin = copy.copy(self.origin)
         aa.n_1    = copy.copy(self.n_1)
         aa.n_2    = copy.copy(self.n_2)
         aa.n_3    = copy.copy(self.n_3)
         aa.step_1 = copy.copy(self.step_1)
         aa.step_2 = copy.copy(self.step_2)
         aa.step_3 = copy.copy(self.step_3)
         aa.atoms  = copy.copy(self.atoms)
         aa.data   = np.array(self.data) - np.array(other.data)
         return aa

     def __mul__(self,other):
         """Defines the '*' operator. Data multiplication of two cubes
            The header of resulting cube is of the left side cube
         """

         aa = cube()
         aa.natoms = copy.copy(self.natoms)
         aa.origin = copy.copy(self.origin)
         aa.n_1    = copy.copy(self.n_1)
         aa.n_2    = copy.copy(self.n_2)
         aa.n_3    = copy.copy(self.n_3)
         aa.step_1 = copy.copy(self.step_1)
         aa.step_2 = copy.copy(self.step_2)
         aa.step_3 = copy.copy(self.step_3)
         aa.atoms  = copy.copy(self.atoms)
         aa.data   = np.array(self.data) * np.array(other.data)
         return aa

     def cdz(self,fname):
         """Charge displacement function over a cube in the Z direction
            return cdz => List[[z_0,cdz(z0),\Delta_rho(z0)],
                               [z_1,cdz(z_1),\Delta_rho(z_1)],
                               [],...]
         """
         f = open(fname,'w')

         ds   = self.step_1[0]*self.step_2[1] # surface element dx*dy
         step = self.step_3[2]
         origin = self.origin[2]
         nstep  = self.n_3
         reduction = (0,1)        # definition of axis reduction here X and Y

         temp = np.reshape(self.data,(self.n_1,self.n_2,self.n_3),order='C')
         risu = np.sum(temp,axis=reduction) 

         temp = []
         risu = risu * ds                 # \Delta \rho(z)
         s = 0. 

         cd =[]
         for i in range(nstep):
             s += risu[i]
             cd.append([origin + i*step, s*step, risu[i]])

         for i in cd:
             f.write(('%e %e %e \n') % (i[0], i[1], i[2]))

         f.close()
         return cd

     def cdy(self,fname):
         """Charge displacement function over a cube in the Y direction
            return cdy => List[[y_0,cdy(y0),\Delta_rho(y0)],
                               [y_1,cdy(y_1),\Delta_rho(y_1)],
                               [],...]
         """
         f = open(fname,'w')

         ds   = self.step_1[0]*self.step_3[2] # surface element dx*dy
         step = self.step_2[1]
         origin = self.origin[1]
         nstep  = self.n_2
         reduction = (0,2)        # definition of axis reduction here X and Y

         temp = np.reshape(self.data,(self.n_1,self.n_2,self.n_3),order='C')
         risu = np.sum(temp,axis=reduction)

         temp = []
         risu = risu * ds                 # \Delta \rho(z)
         s = 0.

         cd =[]
         for i in range(nstep):
             s += risu[i]
             cd.append([origin + i*step, s*step, risu[i]])

         for i in cd:
             f.write(('%e %e %e \n') % (i[0], i[1], i[2]))

         f.close()
         return cd

     def cdx(self,fname):
         """Charge displacement function over a cube in the X direction
            return cdx => List[[x_0,cdx(x0),\Delta_rho(x0)],
                               [x_1,cdx(x_1),\Delta_rho(x_1)],
                               [],...]
         """
         f = open(fname,'w')

         ds   = self.step_2[1]*self.step_3[2] # surface element dy*dz
         step = self.step_1[0]                # dx
         origin = self.origin[0]
         nstep  = self.n_1
         reduction = (1,2)        # definition of axis reduction here X and Y

         temp = np.reshape(self.data,(self.n_1,self.n_2,self.n_3),order='C')
         risu = np.sum(temp,axis=reduction)
         temp = []
         risu = risu * ds                 # \Delta \rho(z)
         s = 0.
         cd =[]
         for i in range(nstep):
             s += risu[i]
             cd.append([origin + i*step, s*step, risu[i]])

         for i in cd:
             f.write(('%e %e %e \n') % (i[0], i[1], i[2]))

         f.close()
         return cd



     def toXYZ(self):
         """ Da completare From cube format to x, y, z, value  format
            output is written on file 'fname' 
         """

         temp = np.reshape(self.data,(self.n_1,self.n_2,self.n_3),order='C')
  
         x = []
         y = []
         z = []
         for i in range(self.n_1):
            for j in range(self.n_2): 
               for k in range(self.n_3):
                   x.append(self.origin[0]+ i*self.step_1[0])
                   y.append(self.origin[1]+ j*self.step_2[1]) 
                   z.append(self.origin[2]+ k*self.step_3[2]) 
                   ss = x,y,z,self.data 
                   aa = np.transpose(ss)
#         for i in aa:
#                  print(('%e %e %e %e \n') % (i[0], i[1], i[2], i[3]))
         np.savetxt('toXYZ.out', aa, fmt='%e', newline='\n')
         return 
    

     def get_grid_xyz(self):
         """ x, y, z, values  of cube grid point 
         """

         x = []
         y = []
         z = []
         for i in range(self.n_1):
                   x.append(self.origin[0]+ i*self.step_1[0])

         for j in range(self.n_2):
                   y.append(self.origin[1]+ j*self.step_2[1])

         for k in range(self.n_3):
                   z.append(self.origin[2]+ k*self.step_3[2])

         return x,y,z


     def integrate(self):

         dv = self.step_1[0]*self.step_2[1]*self.step_3[2]
         risu = sum(self.data)*dv
         return risu 

     def spherical_int(self, center, diameter):
         """ 
         """
         print('I am in spherical')

         x = []
         y = []
         z = []
         dist =[]
         for i in range(self.n_1):
            for j in range(self.n_2): 
               for k in range(self.n_3):
                   x = self.origin[0]+ i*self.step_1[0]
                   y = self.origin[1]+ j*self.step_2[1] 
                   z = self.origin[2]+ k*self.step_3[2] 
                   tmp2 = (x - center[0])**2 + (y - center[1])**2 + (z - center[2])**2 
                   dist.append(math.sqrt(tmp2)) 

         dv = self.step_1[0]*self.step_2[1]*self.step_3[2]
         
         partsum = 0.
         for i in range(len(self.data)) :
             if (dist[i] < diameter):    
               partsum += self.data[i]

#         print('Electronic Charge the sphere ', diameter, partsum*dv)

         return partsum*dv

