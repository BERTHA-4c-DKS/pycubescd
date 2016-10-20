import numpy 
import math
 
class cube:

  def __init__(self, fname):

      self.__atoms = []
      self.__natoms = 0
      self.__nx = 0
      self.__ny = 0
      self.__nz = 0
      self.__data = numpy.zeros((1,1,1))
      self.__origin = numpy.zeros((1,1,1))
      self.__x = numpy.zeros((1,1,1))
      self.__y = numpy.zeros((1,1,1))
      self.__z = numpy.zeros((1,1,1))

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
          self.__atoms.append([line[0], line[2], line[3], line[4]])
        
      self.__data = numpy.zeros((self.__nx,self.__ny,self.__nz))
      i = 0
      for s in f:
          for v in s.split():
              self.__data[i/(self.__ny * self.__nz), \
                  (i/self.__nz)%self.__ny, \
                  i % self.__nz] = float(v)
              i += 1
      
      if i != self.__nx * self.__ny * self.__nz: 
          raise NameError, "Errore while reading cube file"


  def clear(self):
      self.__atoms = []
      self.__natoms = 0
      self.__nx = 0
      self.__ny = 0
      self.__nz = 0
      self.__data = numpy.zeros((1,1,1))
      self.__origin = numpy.zeros((1,1,1))
      self.__x = numpy.zeros((1,1,1))
      self.__y = numpy.zeros((1,1,1))
      self.__z = numpy.zeros((1,1,1))


  def get_natoms(self):
      return self.__natoms


  def get_atoms(self):
      return self.__atoms


  def get_data(self):
      return self.__data


  def get_origin(self):
      return self.__origin


  def get_nx(self):
      return self.__nx


  def get_ny(self):
      return self.__ny


  def get_nz(self):
      return self.__nz


  def get_x(self):
      return self.__x


  def get_y(self):
      return self.__y


  def get_z(self):
      return self.__z


  def get_volume(self):

      vol = (self.__nx - 1) * self.__x[0] * \
            (self.__ny - 1) * self.__y[1] * \
            (self.__nz - 1) * self.__z[2]

      return vol


  def dump(self, f):

      print >> f, "cube file\ngenerated"
      print >> f, "%4d %.6f %.6f %.6f" % \
              (self.__natoms, self.__origin[0], self.__origin[1], \
              self.__origin[2])
      print >> f, "%4d %.6f %.6f %.6f"% \
              (self.__nx, self.__x[0], self.__x[1], self.__x[2])
      print >> f, "%4d %.6f %.6f %.6f"% \
              (self.__ny, self.__y[0], self.__y[1], self.__y[2])
      print >> f, "%4d %.6f %.6f %.6f"% \
              (self.__nz, self.__z[0], self.__z[1], self.__z[2])

      for atom in self.__atoms:
          print >> f, "%s %d %s %s %s" % \
                  (atom[0], 0, atom[1], atom[2], atom[3])
      
      for ix in xrange(self.__nx):
          for iy in xrange(self.__ny):
              for iz in xrange(self.__nz):
                   print >>f, "%.5e " % self.__data[ix,iy,iz],
                   if (iz % 6 == 5): 
                       print >> f, ''
      
              print >> f,  ""
 

  def mask_sphere(self, r, cx, cy, cz):
      # cut a sphere with radius r and center in [cx,cy,cz]
      
      m = 0 * self.__data
      ixmin = int(math.ceil((cx-r)/self.__x[0]))
      ixmax = int(math.floor((cx+r)/self.__x[0]))
      for ix in xrange(ixmin, ixmax):
          ryz = math.sqrt(r**2-(ix*self.__x[0]-cx)**2)
          iymin = int(math.ceil((cy-ryz)/self.__y[1]))
          iymax = int(math.floor((cy+ryz)/self.__y[1]))
        
          for iy in xrange(iymin, iymax):
              rz = math.sqrt(ryz**2 - (iy*self.__y[1]-cy)**2)
              izmin = int(math.ceil((cz-rz)/self.__z[2]))
              izmax = int(math.floor((cz+rz)/self.__z[2])) 
        
              for iz in xrange (izmin, izmax):
                  m[ix,iy,iz] = 1
        
      return m
