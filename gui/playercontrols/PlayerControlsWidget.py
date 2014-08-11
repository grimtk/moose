#!/usr/bin/env python
import os, sys, traceback
from PySide import QtCore, QtGui

from base import *
import qrc_resources

##
# An input file widget
class PlayerControlsWidget(MooseWidget):

  # Define signals that will be emitted from this object
  _signal_back = QtCore.Signal()
  _signal_play = QtCore.Signal()
  _signal_pause = QtCore.Signal()
  _signal_forward = QtCore.Signal()
  _signal_loop = QtCore.Signal()

  def __init__(self, **kwargs):
    MooseWidget.__init__(self, **kwargs)

    self.addObject(QtGui.QHBoxLayout(), handle='PlayerControlsLayout')
    self.object('PlayerControlsLayout').addStretch(1)
    self.addObject(QtGui.QPushButton(QtGui.QIcon(":/backButton.png"), 'Back'), handle='Back', parent='PlayerControlsLayout')
    self.addObject(QtGui.QPushButton(QtGui.QIcon(":/playButton.png"), 'Play'), handle='Play', parent='PlayerControlsLayout')
    self.addObject(QtGui.QPushButton(QtGui.QIcon(":/pauseButton.png"), 'Pause'), handle='Pause', parent='PlayerControlsLayout')
    self.addObject(QtGui.QPushButton(QtGui.QIcon(":/forwardButton.png"), 'Forward'), handle='Forward', parent='PlayerControlsLayout')
    self.addObject(QtGui.QPushButton(QtGui.QIcon(":/loopButton.png"), 'Loop'), handle='Loop', parent='PlayerControlsLayout')

    # Run the setup methods
    self.setup()

    ## DEMO INFO ##
    self.info()

  ##
  # Executes when 'Back' button is pressed (auto connected via addObject)
  def _callbackBack(self):
    print  >> sys.stderr,'_callbackBack'
    self._signal_back.emit()

  ##
  # Executes when 'Play' button is pressed
  def _callbackPlay(self):
    print >> sys.stderr, '_callbackPlay'
    self._signal_play.emit()

  ##
  # Executes when 'Pause' button is pressed
  def _callbackPause(self):
    print  >> sys.stderr,'_callbackPause'
    self._signal_pause.emit()

  ##
  # Executes when 'Forward' button is pressed
  def _callbackForward(self):
    print  >> sys.stderr,'_callbackForward'
    self._signal_forward.emit()

  ##
  # Executes when 'Loop' button is pressed
  def _callbackLoop(self):
    print  >> sys.stderr,'_callbackLoop'
    self._signal_loop.emit()

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

