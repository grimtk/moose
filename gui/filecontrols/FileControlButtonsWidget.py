#!/usr/bin/env python
import os, sys, traceback

from PySide import QtCore, QtGui

from base import *

##
# An input file widget
class FileControlButtonsWidget(MooseWidget):

  # Define signals that will be emitted from this object
  _signal_open = QtCore.Signal(str)
  _signal_save = QtCore.Signal(str)
  _signal_reset = QtCore.Signal()

  def __init__(self, **kwargs):
    MooseWidget.__init__(self, **kwargs)

    self.addObject(QtGui.QFrame(), handle='Frame')
    self.object('Frame').setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Raised)
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
  # Setup the 'Open' file button (auto called via setup())
  #def _setupOpen(self, q_object):
  #  q_object.setToolTip('Open existing plot file')
    #q_object.property('label').setAlignment(QtCore.Qt.AlignCenter)

  ##
  # Setup the 'Save' file button (auto called via setup())
  #def _setupSave(self, q_object):
  #  q_object.setToolTip('Save a plot file')
    #q_object.property('label').setAlignment(QtCore.Qt.AlignCenter)

  ##
  # Setup the 'Reset' button (auto called via setup())
  #def _setupReset(self, q_object):
  #  q_object.setToolTip('Reset plot to start')
    #q_object.property('FileControlButtonLayout').setAlignment(QtCore.Qt.AlignCenter)

