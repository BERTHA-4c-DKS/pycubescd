

import numpy 
import math
import os
from io import open

class atom(object): 

  def __init__(self, zin, charge, x, y, z):
    self.__z = zin
    self.__coordinates = (x, y, z)
    self.__charge = charge
  
  def set_Z(self, zin): 
    self.__z = zin
  
  def get_Z(self):
    return self.__z

  def set_coordinates(self, x, y, z):
    self.__coordinates = (x, y, z)

  def get_x(self):
    return self.__coordinates[0]

  def get_y(self):
    return self.__coordinates[1]

  def get_z(self):
    return self.__coordinates[2]

  def get_coordinates(self):
    return self.__coordinates

  def set_charge (self, charge):
    self.__charge = charge

  def get_charge (self):
    return self.__charge

  def get_str(self):
    return '%4d %10.6f %10.6f %10.6f %10.6f' % (self.__z, 
        self.__charge, self.__coordinates[0], self.__coordinates[1],
        self.__coordinates[2])

  def __repr__(self): # overloads printing
    return self.get_str()
 
class cube(object):
  
  def __init__(self, fname=""):

      self.__atoms = []
      self.__natoms = 0
      self.__nx = 0
      self.__ny = 0
      self.__nz = 0
      self.__data = numpy.zeros((1,1,1))
      self.__rawdata = []
      self.__origin = numpy.zeros((1,1,1))
      self.__x = numpy.zeros((1,1,1))
      self.__y = numpy.zeros((1,1,1))
      self.__z = numpy.zeros((1,1,1))

      if fname != "":
          self.readfile(fname)

  def readfile (self, fname):

      self.clear()
      
      f = open(fname, 'r')
      
      for i in range(2): 
          f.readline() 
      
      line = f.readline().split() 
      self.__natoms = int(line[0])
      self.__origin = numpy.array([float(line[1]), \
          float(line[2]), \
          float(line[3])]) 
      
      line = f.readline().split() 
      self.__nx = int(line[0])
      self.__x = numpy.array([float(line[1]), \
              float(line[2]), \
              float(line[3])])
      
      line = f.readline().split() 
      self.__ny = int(line[0])
      self.__y = numpy.array([float(line[1]), \
              float(line[2]), \
              float(line[3])])
      
      line = f.readline().split() 
      self.__nz = int(line[0])
      self.__z = numpy.array([float(line[1]), \
              float(line[2]), \
              float(line[3])])
      
      for i in range(self.__natoms):
          line = f.readline().split()
          a = atom(int(line[0]), float(line[1]),  float(line[2]), \
                float(line[3]),  float(line[4]))
          self.__atoms.append(a)
        
      self.__data = numpy.zeros((self.__nx,self.__ny,self.__nz))
      i = 0
      for s in f:
          for v in s.split():
              self.__rawdata.append(float(v)) 
              self.__data[int(i/(self.__ny * self.__nz)), \
                  int((i/self.__nz)%self.__ny), \
                  int(i % self.__nz)] = float(v)
              i += 1
      
      if i != self.__nx * self.__ny * self.__nz: 
          raise SizeError("Errore while reading cube file")


  def clear(self):
      self.__atoms = []
      self.__natoms = 0
      self.__nx = 0
      self.__ny = 0
      self.__nz = 0
      self.__data = numpy.zeros((1,1,1))
      self.__rawdata[:] = []
      self.__origin = numpy.zeros((1,1,1))
      self.__x = numpy.zeros((1,1,1))
      self.__y = numpy.zeros((1,1,1))
      self.__z = numpy.zeros((1,1,1))

  def set_data(self, newd):
      self.__data = newd

      self.__nx = self.__data.shape[0]
      self.__ny = self.__data.shape[1]
      self.__nz = self.__data.shape[2]

  def set_rawdata(self, newd):
      self.__rawdata = newd

  def set_origin(self, x, y, z):
      self.__origin = numpy.array([x, y, z])

  def set_x(self, x):
      self.__x = x

  def set_y(self, y):
      self.__y = y

  def set_z(self, z):
      self.__z = z

  def set_atoms(self, at):
      self.__atoms = at
      self.__natoms = len(at)

  def get_natoms(self):
      return self.__natoms

  def get_atoms(self):
      return self.__atoms

  def get_data(self):
      return self.__data

  def get_rawdata(self):
      return self.__rawdata

  def get_origin(self):
      return self.__origin

  def get_nx(self):
      return self.__nx

  def get_ny(self):
      return self.__ny

  def get_nz(self):
      return self.__nz

  def get_dx(self):
      return self.__x[0]

  def get_dy(self):
      return self.__y[1]

  def get_dz(self):
      return self.__z[2]

  def get_x(self):
      return self.__x

  def get_y(self):
      return self.__y

  def get_z(self):
      return self.__z

  def cd (self, ax = "x", fname=""):

      if ax == "z":
          return self.cdz(fname)
      elif ax == "x":
          return self.cdx(fname)
      elif ax == "y":
          return self.cdy(fname)
 
  def cdy (self, fname=""):
      cd = []

      ymin = self.get_origin()[1]
      dy = self.get_dy()
      vals = self.integrate("y")
      i = 1 
      for v in vals:
          cd.append([ymin+(i-1)*dy, numpy.sum( vals[:i] ) * dy, v])
          i = i + 1

      if fname != "":
         if os.path.exists(fname):
             os.remove(fname)

         f = open(fname,'w')

         for i in cd:
             f.write(('%e %e %e \n') % (i[0], i[1], i[2]))

         f.close()
      
      return cd

  def cdx (self, fname=""):
      cd = []

      xmin = self.get_origin()[0]
      dx = self.get_dx()
      vals = self.integrate("x")
      i = 1
      for v in vals:
          cd.append([xmin+(i-1)*dx, numpy.sum( vals[:i] ) * dx, v])
          i = i + 1

      if fname != "":
         if os.path.exists(fname):
             os.remove(fname)

         f = open(fname,'w')

         for i in cd:
             f.write(('%e %e %e \n') % (i[0], i[1], i[2]))

         f.close()
       
      return cd

  def cdz (self, fname=""):
      cd = []

      zmin = self.get_origin()[2]
      dz = self.get_dz()
      vals = self.integrate("z")
      i = 1 
      for v in vals:
          cd.append([zmin+(i-1)*dz, numpy.sum( vals[:i] ) * dz, v])
          i = i + 1

      if fname != "":
         if os.path.exists(fname):
             os.remove(fname)

         f = open(fname,'w')

         for i in cd:
             f.write(('%e %e %e \n') % (i[0], i[1], i[2]))

         f.close()
       
      return cd

  def integrate (self, axis=""):

      if axis == "":
          itgr = numpy.sum(self.__data) * self.get_dx() * self.get_dy() * \
                  self.get_dz()
          return itgr
      elif axis == "z":
          itgr = numpy.sum(self.__data, axis=(0,1)) * self.get_dx() * self.get_dy()
          return itgr
      elif axis == "x":
          itgr = numpy.sum(self.__data, axis=(1,2)) * self.get_dy() * self.get_dz()
          return itgr
      elif axis == "y":
          itgr = numpy.sum(self.__data, axis=(0,2)) * self.get_dx() * self.get_dz()
          return itgr

      return None

  def get_volume(self):

      vol = (self.__nx - 1) * self.get_x() * \
            (self.__ny - 1) * self.get_y() * \
            (self.__nz - 1) * self.get_z()

      return vol

  def get_str(self):

      str = "%4d %.6f %.6f %.6f\n" % \
              (self.__natoms, self.__origin[0], self.__origin[1], \
              self.__origin[2])
      str += "%4d %.6f %.6f %.6f\n"% \
              (self.__nx, self.__x[0], self.__x[1], self.__x[2])
      str += "%4d %.6f %.6f %.6f\n"% \
              (self.__ny, self.__y[0], self.__y[1], self.__y[2])
      str += "%4d %.6f %.6f %.6f\n"% \
              (self.__nz, self.__z[0], self.__z[1], self.__z[2])

      for a in self.__atoms:
          str += a.get_str() + "\n"
      
      for ix in range(self.__nx):
          for iy in range(self.__ny):
              for iz in range(self.__nz):
                   str += "%.5e \n"% self.__data[ix,iy,iz]
      
      return str

  def __add__ (self, b):

      if (self.get_nx() != b.get_nx()) or (self.get_ny() != b.get_ny()) or \
         (self.get_nz() != b.get_nz()) or (self.get_dx() != b.get_dx()) or \
         (self.get_dy() != b.get_dy()) or (self.get_dz() != b.get_dz()) or \
         (self.get_origin()[0] != b.get_origin()[0]) or \
         (self.get_origin()[1] != b.get_origin()[1]) or \
         (self.get_origin()[2] != b.get_origin()[2]):
        raise SizeError("cubes are not compatible")
      
      retc = cube()

      retc.set_origin(self.get_origin()[0], self.get_origin()[1], \
              self.get_origin()[2])

      retc.set_atoms(self.__atoms)

      newd = self.get_data()
      newd_raw = self.get_rawdata()

      for i in range(len(newd_raw)):
          newd_raw[i] += b.get_rawdata()[i]

      for ix in range(self.__nx):
          for iy in range(self.__ny):
              for iz in range(self.__nz):
                   newd[ix,iy,iz] += b.get_data()[ix,iy,iz] 

      retc.set_data(newd)
      retc.set_rawdata(newd_raw)

      retc.set_x(self.get_x())
      retc.set_y(self.get_y())
      retc.set_z(self.get_z())

      return retc

  def __sub__ (self, b):

      if (self.get_nx() != b.get_nx()) or (self.get_ny() != b.get_ny()) or \
         (self.get_nz() != b.get_nz()) or (self.get_dx() != b.get_dx()) or \
         (self.get_dy() != b.get_dy()) or (self.get_dz() != b.get_dz()) or \
         (self.get_origin()[0] != b.get_origin()[0]) or \
         (self.get_origin()[1] != b.get_origin()[1]) or \
         (self.get_origin()[2] != b.get_origin()[2]):
        raise SizeError("cubes are not compatible")
      
      retc = cube()

      retc.set_origin(self.get_origin()[0], self.get_origin()[1], \
              self.get_origin()[2])

      retc.set_atoms(self.__atoms)

      newd = self.get_data()
      newd_raw = self.get_rawdata()

      for i in range(len(newd_raw)):
          newd_raw[i] -= b.get_rawdata()[i]

      for ix in range(self.__nx):
          for iy in range(self.__ny):
              for iz in range(self.__nz):
                   newd[ix,iy,iz] -= b.get_data()[ix,iy,iz] 

      retc.set_data(newd)
      retc.set_rawdata(newd_raw)

      retc.set_x(self.get_x())
      retc.set_y(self.get_y())
      retc.set_z(self.get_z())

      return retc

  def __mul__ (self, b):

      if (self.get_nx() != b.get_nx()) or (self.get_ny() != b.get_ny()) or \
         (self.get_nz() != b.get_nz()) or (self.get_dx() != b.get_dx()) or \
         (self.get_dy() != b.get_dy()) or (self.get_dz() != b.get_dz()) or \
         (self.get_origin()[0] != b.get_origin()[0]) or \
         (self.get_origin()[1] != b.get_origin()[1]) or \
         (self.get_origin()[2] != b.get_origin()[2]):
        raise SizeError("cubes are not compatible")
      
      retc = cube()

      retc.set_origin(self.get_origin()[0], self.get_origin()[1], \
              self.get_origin()[2])

      retc.set_atoms(self.__atoms)

      newd = self.get_data()
      newd_raw = self.get_rawdata()

      for i in range(len(newd_raw)):
          newd_raw[i] = self.get_rawdata()[i] *\
                  b.get_rawdata()[i]

      for ix in range(self.__nx):
          for iy in range(self.__ny):
              for iz in range(self.__nz):
                   newd[ix,iy,iz] = self.get_data()[ix,iy,iz] * \
                           b.get_data()[ix,iy,iz] 

      retc.set_data(newd)
      retc.set_rawdata(newd_raw)

      retc.set_x(self.get_x())
      retc.set_y(self.get_y())
      retc.set_z(self.get_z())

      return retc

  def __repr__ (self):

      str = "cube file\ngenerated\n"
      str += self.get_str()
      
      return str

  def dump(self, f):

      print("cube file\ngenerated", file=f)
      print(self.get_str(), file=f)

  def to_xyz (self, fname = "toXYZ.out"):

      temp = numpy.reshape(self.__rawdata, \
              (self.__nx*self.__ny*self.__nz), order='C')
  
      x = []
      y = []
      z = []
      for i in range(self.__nx):
         for j in range(self.__ny): 
            for k in range(self.__nz):
                x.append(self.__origin[0] + i * self.__x[0])
                y.append(self.__origin[1] + j * self.__y[1]) 
                z.append(self.__origin[2] + k * self.__z[2]) 
                ss = x, y, z, temp
                aa = numpy.transpose(ss)

      numpy.savetxt(fname, aa, fmt='%e', newline='\n')
  
  def get_grid_xyz(self):

      x = []
      y = []
      z = []

      for i in range(self.__nx):
          x.append(self.__origin[0] + i * self.__x[0])

      for j in range(self.__ny):
          y.append(self.__origin[1] + j * self.__y[1])

      for k in range(self.__nz):
          z.append(self.__origin[2] + k * self.__z[2])

      return x, y, z

  def get_xminmax(self):
      xmin = self.__origin[0]
      xmax = self.__origin[0] + (self.__nx - 1) * self.__x[0]

      return xmin, xmax

  def get_yminmax(self):
      ymin = self.__origin[1]
      ymax = self.__origin[1] + (self.__ny - 1) * self.__y[1]

      return ymin, ymax

  def get_zminmax(self):
      zmin = self.__origin[2]
      zmax = self.__origin[2] + (self.__nz - 1) * self.__z[2]

      return zmin, zmax

  def get_enclosed_r (self, center, axis="N"):

      x = center[0]
      y = center[1]
      z = center[2]

      xmin, xmax = self.get_xminmax()
      ymin, ymax = self.get_yminmax()
      zmin, zmax = self.get_zminmax()

      if (x < xmax) and (x > xmin):
          if (y > ymin) and (y < ymax):
              if (z > zmin) and (z < zmax):
                  if axis == "N":
                      rx = min(x - xmin, xmax - x)
                      ry = min(y - ymin, ymax - y)
                      rz = min(z - zmin, zmax - z)
                  elif axis == "z":
                      rx = min(x - xmin, xmax - x)
                      ry = min(y - ymin, ymax - y)
                      rz = zmax - z
                  elif axis == "mz":
                      rx = min(x - xmin, xmax - x)
                      ry = min(y - ymin, ymax - y)
                      rz = z - zmin
                  elif axis == "y":
                      rx = min(x - xmin, xmax - x)
                      ry = ymax - y
                      rz = min(z - zmin, zmax - z)
                  elif axis == "my":
                      rx = min(x - xmin, xmax - x)
                      ry = y - ymin
                      rz = min(z - zmin, zmax - z)
                  elif axis == "x":
                      rx = xmax - x
                      ry = min(y - ymin, ymax - y)
                      rz = min(z - zmin, zmax - z)
                  elif axis == "mx":
                      rx = x - xmin
                      ry = min(y - ymin, ymax - y)
                      rz = min(z - zmin, zmax - z)

                  return min(rx, min(ry, rz))

      return None

  def spherical_int_rdr(self, center, rmax, dr, axis="N", angle=180):

      nstep = int(rmax/dr) - 1

      dim = self.__nx * self.__ny * self.__nz

      a = 0
      ltrip = []
      lvectors = []
      dist = numpy.zeros(dim)
      xval = numpy.zeros(dim)
      yval = numpy.zeros(dim)
      zval = numpy.zeros(dim)
      for i in range(self.__nx):
         for j in range(self.__ny): 
            for k in range(self.__nz):
                x = self.__origin[0] + i * self.__x[0]
                y = self.__origin[1] + j * self.__y[1] 
                z = self.__origin[2] + k * self.__z[2] 
                tmp2 = (x - center[0])**2 + (y - center[1])**2 + (z - center[2])**2 
                dist[a] = math.sqrt(tmp2)
                xval[a] = x
                yval[a] = y
                zval[a] = z
                ltrip.append((i, j, k))
                lvectors.append((x, y, z))
                a = a + 1

      trip = numpy.asarray(ltrip)
      vectors = numpy.asarray(lvectors)
      dv = self.__x[0] * self.__y[1] * self.__z[2]
      
      r = 0.0
      rv = []

      if axis == "N":
          for i in range(0, nstep):
              vals = trip[(dist >= r) & (dist < r + dr)]
              summa = 0.0
              for v in vals:
                  summa += self.__data[v[0],v[1],v[2]]
              rv.append(summa*dv)
              r = r + dr
      else:
          newdist = dist
          newtrip = trip
          if axis == "x":
              if angle >= 90:
                  newdist = dist[( xval > center[0])]
                  newtrip = trip[( xval > center[0])]
              else:
                  if center[0] != 0.0 or center[1] != 0.0 or center[2] != 0.0 :
                      return None

                  normvectors = numpy.array([numpy.linalg.norm(v) for v in vectors]) 
                  dotprod = numpy.array([(v[0]*1.0 + v[1]*0.0 + v[2]*0.0) for v in vectors])
                  cosangle = dotprod/normvectors
                  angles =  numpy.absolute(numpy.arccos(cosangle) * (180.0/math.pi))

                  newdist = dist[( xval > 0.0) & (angles <= angle)]
                  newtrip = trip[( xval > 0.0) & (angles <= angle)]
          elif axis == "mx":
              if angle >= 90 :
                  newdist = dist[( xval < center[0])]
                  newtrip = trip[( xval < center[0])]
              else:
                  if center[0] != 0.0 or center[1] != 0.0 or center[2] != 0.0 :
                      return None

                  normvectors = numpy.array([numpy.linalg.norm(v) for v in vectors]) 
                  dotprod = numpy.array([(v[0]*-1.0 + v[1]*0.0 + v[2]*0.0) for v in vectors])
                  cosangle = dotprod/normvectors
                  angles =  numpy.absolute(numpy.arccos(cosangle) * (180.0/math.pi))

                  newdist = dist[( xval < 0.0) & (angles <= angle)]
                  newtrip = trip[( xval < 0.0) & (angles <= angle)]
          elif axis == "y":
              if angle >= 90 :
                  newdist = dist[( yval > center[1])]
                  newtrip = trip[( yval > center[1])]
              else:
                  if center[0] != 0.0 or center[1] != 0.0 or center[2] != 0.0 :
                      return None

                  normvectors = numpy.array([numpy.linalg.norm(v) for v in vectors]) 
                  dotprod = numpy.array([(v[0]*0.0 + v[1]*1.0 + v[2]*0.0) for v in vectors])
                  cosangle = dotprod/normvectors
                  angles =  numpy.absolute(numpy.arccos(cosangle) * (180.0/math.pi))

                  newdist = dist[( yval > 0.0) & (angles <= angle)]
                  newtrip = trip[( yval > 0.0) & (angles <= angle)]
          elif axis == "my":
              if angle >= 90 :
                  newdist = dist[( yval < center[1])]
                  newtrip = trip[( yval < center[1])]
              else:
                  if center[0] != 0.0 or center[1] != 0.0 or center[2] != 0.0 :
                      return None

                  normvectors = numpy.array([numpy.linalg.norm(v) for v in vectors]) 
                  dotprod = numpy.array([(v[0]*0.0 + v[1]*-1.0 + v[2]*0.0) for v in vectors])
                  cosangle = dotprod/normvectors
                  angles =  numpy.absolute(numpy.arccos(cosangle) * (180.0/math.pi))

                  newdist = dist[( yval < 0.0) & (angles <= angle)]
                  newtrip = trip[( yval < 0.0) & (angles <= angle)]
          elif axis == "z":
              if angle >= 90 :
                  newdist = dist[( zval > center[2])]
                  newtrip = trip[( zval > center[2])]
              else:
                  if center[0] != 0.0 or center[1] != 0.0 or center[2] != 0.0 :
                      return None

                  normvectors = numpy.array([numpy.linalg.norm(v) for v in vectors]) 
                  dotprod = numpy.array([(v[0]*0.0 + v[1]*0.0 + v[2]*1.0) for v in vectors])
                  cosangle = dotprod/normvectors
                  angles =  numpy.absolute(numpy.arccos(cosangle) * (180.0/math.pi))

                  newdist = dist[( zval > 0.0) & (angles <= angle)]
                  newtrip = trip[( zval > 0.0) & (angles <= angle)]
          elif axis == "mz":
              if angle >= 90 :
                  newdist = dist[( zval < center[2])]
                  newtrip = trip[( zval < center[2])]
              else:
                  if center[0] != 0.0 or center[1] != 0.0 or center[2] != 0.0 :
                      return None

                  normvectors = numpy.array([numpy.linalg.norm(v) for v in vectors]) 
                  dotprod = numpy.array([(v[0]*0.0 + v[1]*0.0 + v[2]*-1.0) for v in vectors])
                  cosangle = dotprod/normvectors
                  angles =  numpy.absolute(numpy.arccos(cosangle) * (180.0/math.pi))

                  newdist = dist[( zval < 0.0) & (angles <= angle)]
                  newtrip = trip[( zval < 0.0) & (angles <= angle)]
          else:
              return None

          for i in range(0, nstep):
              vals = newtrip[(newdist >= r) & (newdist < r + dr)]
              summa = 0.0
              for v in vals:
                  summa += self.__data[v[0],v[1],v[2]]
              rv.append(summa*dv)
              r = r + dr

      return rv

  def spherical_intdr(self, center, r, dr):

      dist = []
      for i in range(self.__nx):
         for j in range(self.__ny): 
            for k in range(self.__nz):
                x = self.__origin[0] + i * self.__x[0]
                y = self.__origin[1] + j * self.__y[1] 
                z = self.__origin[2] + k * self.__z[2] 
                tmp2 = (x - center[0])**2 + (y - center[1])**2 + (z - center[2])**2 
                dist.append(math.sqrt(tmp2)) 

      dv = self.__x[0] * self.__y[1] * self.__z[2]
      
      summa = 0.0
      a = 0
      for i in range(self.__nx):
         for j in range(self.__ny): 
            for k in range(self.__nz):
                if (dist[a] >= r) and (dist[a] < (r+dr)):    
                    summa += self.__data[i,j,k]
                a = a + 1

      return summa * dv

  def spherical_int(self, center, diameter):

      dist = []
      for i in range(self.__nx):
         for j in range(self.__ny): 
            for k in range(self.__nz):
                x = self.__origin[0] + i * self.__x[0]
                y = self.__origin[1] + j * self.__y[1] 
                z = self.__origin[2] + k * self.__z[2] 
                tmp2 = (x - center[0])**2 + (y - center[1])**2 + (z - center[2])**2 
                dist.append(math.sqrt(tmp2)) 

      dv = self.__x[0] * self.__y[1] * self.__z[2]
      
      summa = 0.0
      a = 0
      for i in range(self.__nx):
         for j in range(self.__ny): 
            for k in range(self.__nz):
                if (dist[a] < diameter):    
                    summa += self.__data[i,j,k]
                a = a + 1

      return summa * dv

  def mask_sphere(self, r, cx, cy, cz):
      # cut a sphere with radius r and center in [cx,cy,cz]
      
      m = 0 * self.__data
      ixmin = int(math.ceil((cx-r)/self.__x[0]))
      ixmax = int(math.floor((cx+r)/self.__x[0]))
      for ix in range(ixmin, ixmax):
          ryz = math.sqrt(r**2-(ix*self.__x[0]-cx)**2)
          iymin = int(math.ceil((cy-ryz)/self.__y[1]))
          iymax = int(math.floor((cy+ryz)/self.__y[1]))
        
          for iy in range(iymin, iymax):
              rz = math.sqrt(ryz**2 - (iy*self.__y[1]-cy)**2)
              izmin = int(math.ceil((cz-rz)/self.__z[2]))
              izmax = int(math.floor((cz+rz)/self.__z[2])) 
        
              for iz in range (izmin, izmax):
                  m[ix,iy,iz] = 1
        
      return m
