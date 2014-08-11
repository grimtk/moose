#!/usr/bin/env python
import os, sys, traceback

from PySide import QtCore, QtGui

from base import *

##
# A widget to set axis properties
class AxisSettingsWidget(MooseWidget):

  # Define signals that will be emitted from this object
  _signal_open = QtCore.Signal(str)
  _signal_save = QtCore.Signal(str)
  _signal_reset = QtCore.Signal()

  def __init__(self, **kwargs):
    MooseWidget.__init__(self, **kwargs)

    self.addObject(QtGui.QFrame(), handle='Frame')
    self.object('Frame').setFrameStyle(QtGui.QFrame.StyledPanel | QtGui.QFrame.Raised)
    self.addObject(QtGui.QVBoxLayout(), handle='AxisSettingsLayout', parent='Frame')
    # X Axis
    self.addObject(QtGui.QFrame(), handle='xAxisFrame', parent='AxisSettingsLayout')
    self.object('xAxisFrame').setFrameStyle(QtGui.QFrame.StyledPanel | QtGui.QFrame.Raised)
    self.addObject(QtGui.QVBoxLayout(), handle='xAxisBox', parent='xAxisFrame')
    self.addObject(QtGui.QLabel('X Axis'), handle='xAxisLabel', parent='xAxisBox')
    self.addObject(QtGui.QHBoxLayout(), handle='xAxisVarBox', parent='xAxisBox')
    self.addObject(QtGui.QLabel('Variable'), handle='xAxisVarLabel', parent='xAxisVarBox')
    self.addObject(QtGui.QPushButton('None'), handle='xAxisVar', parent='xAxisVarBox')
    self.addObject(QtGui.QHBoxLayout(), handle='xAxisMinBox', parent='xAxisBox')
    self.addObject(QtGui.QLabel('Min'), handle='xAxisMinLabel', parent='xAxisMinBox')
    self.addObject(QtGui.QLineEdit(), handle='xAxismin', parent='xAxisMinBox')
    self.addObject(QtGui.QHBoxLayout(), handle='xAxisMaxBox', parent='xAxisBox')
    self.addObject(QtGui.QLabel('Max'), handle='xAxisMaxLabel', parent='xAxisMaxBox')
    self.addObject(QtGui.QLineEdit(), handle='xAxismax', parent='xAxisMaxBox')
    # Y Axis
    self.addObject(QtGui.QFrame(), handle='yAxisFrame', parent='AxisSettingsLayout')
    self.object('yAxisFrame').setFrameStyle(QtGui.QFrame.StyledPanel | QtGui.QFrame.Raised)
    self.addObject(QtGui.QVBoxLayout(), handle='yAxisBox', parent='yAxisFrame')
    self.addObject(QtGui.QLabel('Y Axis'), handle='yaxisLabel', parent='yAxisBox')
    self.addObject(QtGui.QHBoxLayout(), handle='yAxisVarBox', parent='yAxisBox')
    self.addObject(QtGui.QLabel('Variable'), handle='yAxisVarLabel', parent='yAxisVarBox')
    self.addObject(QtGui.QPushButton('None'), handle='yAxisVar', parent='yAxisVarBox')
    self.addObject(QtGui.QHBoxLayout(), handle='yAxisMinBox', parent='yAxisBox')
    self.addObject(QtGui.QLabel('Min'), handle='yAxisMinLabel', parent='yAxisMinBox')
    self.addObject(QtGui.QLineEdit(), handle='yAxismin', parent='yAxisMinBox')
    self.addObject(QtGui.QHBoxLayout(), handle='yAxisMaxBox', parent='yAxisBox')
    self.addObject(QtGui.QLabel('Max'), handle='yAxisMaxLabel', parent='yAxisMaxBox')
    self.addObject(QtGui.QLineEdit(), handle='yAxismax', parent='yAxisMaxBox')
    #self.object('FileControlButtonLayout').addStretch(1)

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

