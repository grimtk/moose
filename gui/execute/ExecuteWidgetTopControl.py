import os, sys, traceback
from PySide import QtCore, QtGui

from base import *
<<<<<<< HEAD

##
# Defines the top control buttons for the Execute Tab
class ExecuteWidgetTopControl(PeacockWidget):
  ## Emitted when 'Run' button is pressed
  signal_run = QtCore.Signal(str, str, str, str)

# public:
  def __init__(self, **kwargs):
    PeacockWidget.__init__(self, **kwargs)
=======
from utils import *

##
# Defines the top control buttons for the Execute Tab
class ExecuteWidgetTopControl(MooseWidget):
  ## Emitted when 'Run' button is pressed
  _signal_run = QtCore.Signal(str, str, str, str)

# public:
  def __init__(self, **kwargs):
    MooseWidget.__init__(self, **kwargs)
>>>>>>> a15481f2f7702504bbc9d12841188a339cee5df3

    # Define the mpi/threads/run controls
    self.addObject(QtGui.QHBoxLayout(), handle='ControlButtonLayout')
    self.object('ControlButtonLayout').addStretch(1)
    self.addObject(QtGui.QLineEdit(), handle='MPI', parent='ControlButtonLayout', label='MPI:')
    self.addObject(QtGui.QLineEdit(), handle='Threads', parent='ControlButtonLayout', label='Threads:')
    self.addObject(QtGui.QPushButton('Run'), handle='Run', parent='ControlButtonLayout')

    # The executable edit box and select dialog
    self.addObject(QtGui.QHBoxLayout(), handle='ControlExecutableLayout')
    self.addObject(QtGui.QLineEdit(), handle='Executable', parent='ControlExecutableLayout',
                   label='Current Executable:')
    self.addObject(QtGui.QPushButton('Select'), handle='Select', parent='ControlExecutableLayout')

    # Additional arguments box
    self.addObject(QtGui.QHBoxLayout(), handle='ArgumentsLayout')
    self.addObject(QtGui.QLineEdit(), handle='Arguments', parent='ArgumentsLayout',
                   label='Additional Command Arguments:')

    # Run the setup methods
    self.setup()

    ## DEMO INFO ##
    self.info()

<<<<<<< HEAD
# private:
=======
# protected:
>>>>>>> a15481f2f7702504bbc9d12841188a339cee5df3

  ##
  # Executes when 'Run' is clicked (auto connected via addObject)
  def _callbackRun(self):
    executable = self.object('Executable').text()
    mpi = self.object('MPI').text()
    threads = self.object('Threads').text()
    args = self.object('Arguments').text()
<<<<<<< HEAD
    self.signal_run.emit(executable, mpi, threads, args)
=======
    self._signal_run.emit(executable, mpi, threads, args)
>>>>>>> a15481f2f7702504bbc9d12841188a339cee5df3

  ##
  # Executes when 'Select' button is pressed (auto connected via addObject)
  def _callbackSelect(self):
    file_name = QtGui.QFileDialog.getOpenFileName(self, 'Select Executable...')
    self.object('Executable').setText(file_name[0])

  ##
  # Setups the MPI control and label (auto called via setup())
  def _setupMPI(self, q_object):
    q_object.setMaximumWidth(40)
    q_object.setToolTip('Number of MPI processes to be used.')
    q_object.property('label').setAlignment(QtCore.Qt.AlignRight)

  ##
  # Setups the threads control and label (auto called via setup())
  def _setupThreads(self, q_object):
    q_object.setMaximumWidth(40)
    q_object.setToolTip('Number of threads to be used.')
    q_object.property('label').setAlignment(QtCore.Qt.AlignRight)
<<<<<<< HEAD
=======

  ## A simple test of the pull functionality
  #
  def _pullExecInfo(self, *args):
    txt = self.object('Executable').text()
    if len(args) > 0:
      txt += ' ' + args[0]
    return txt
>>>>>>> a15481f2f7702504bbc9d12841188a339cee5df3
