from PyQt4 import QtGui, QtCore 

import scipy.io
import numpy
import os

import os.path

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

class main_window(QtGui.QMainWindow):
    
    def __init__(self):
        QtGui.QMainWindow.__init__(self) 
        self.resize(640, 480) 
        self.setWindowTitle('PyCD GUI')
        self.statusBar().showMessage('pycd started') 

