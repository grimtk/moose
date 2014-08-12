#!/usr/bin/env python
import os, sys, traceback

from PySide import QtCore, QtGui
import matplotlib.pyplot as plt
import numpy as np

from base import *

##
# An input file widget
class PlotWidget(MooseWidget):

  # Define signals that will be emitted from this object
  _signal_open = QtCore.Signal(str)
  _signal_save = QtCore.Signal(str)
  _signal_reset = QtCore.Signal()

  def __init__(self, **kwargs):
    MooseWidget.__init__(self, **kwargs)

    self.addObject(QtGui.QFrame(), handle='Frame')
    self.object('Frame').setFrameStyle(QtGui.QFrame.StyledPanel | QtGui.QFrame.Raised)
    self.addObject(QtGui.QHBoxLayout(), handle='FileControlButtonLayout', parent='Frame')
    #self.object('FileControlButtonLayout').addStretch(1)
    self.addObject(QtGui.QPushButton('&Open'), handle='Open', parent='FileControlButtonLayout')
    self.addObject(QtGui.QPushButton('&Save'), handle='Save', parent='FileControlButtonLayout')
    self.addObject(QtGui.QPushButton('Reset'), handle='Reset', parent='FileControlButtonLayout')

    # Run the setup methods
    self.setup()

    ## DEMO INFO ##
    self.info()

  ##
  # Executes when 'Open' button is pressed (auto connected via addObject)
  def _callbackOpen(self):
    print  >> sys.stderr,'_callbackOpen'
    file_name = QtGui.QFileDialog.getOpenFileName(self, 'Select plot file...')
    print  >> sys.stderr,'file_name=', file_name[0]
    self._signal_open.emit(file_name[0])

  ##
  # Executes when 'Save' button is pressed
  def _callbackSave(self):
    print >> sys.stderr, '_callbackSave'
    save_file_name = QtGui.QFileDialog.getSaveFileName(self, 'Select plot file to save...')
    print >> sys.stderr, 'save_file_name=', save_file_name[0]
    self._signal_save.emit(save_file_name[0])

  ##
  # Executes when 'Reset' button is pressed
  def _callbackReset(self):
    print  >> sys.stderr,'_callbackReset'
    self._signal_reset.emit()

  ##
  # The plot function that actually shows the plot
  def _Plot(self, q_object):
    q_object.show()

  ##
  # Setup sample plot for demonstration purposes
  def _setupSample(self, q_object):
    q_object.plot()
    q_object.xlim()                       # get current x limits in a list
    q_object.ylim()                       # get current y limits in a list
    q_object.axis([xmin,xmax,ymin,ymax])  # set new axis limits
    q_object.xlabel('This is the X axis')
    q_object.ylabel('This is the Y axis')
    q_object.title('Demo Plot')
    q_object.grid(True)
    q_object.legend()
    self._Plot(q_object)                  # Display the plot
    #q_object.property('label').setAlignment(QtCore.Qt.AlignCenter)

  ##
  # Setup the 'Reset' button (auto called via setup())
  #def _setupReset(self, q_object):
  #  q_object.setToolTip('Reset plot to start')
    #q_object.property('FileControlButtonLayout').setAlignment(QtCore.Qt.AlignCenter)

