import os, sys
from PySide import QtCore, QtGui

from base import *
from filecontrols import *

##
# The Peacock-2 Postprocessor Tab
class PostprocessorWidget(MooseWidget):

# public:
  def __init__(self, **kwargs):
    MooseWidget.__init__(self, **kwargs)

    # Add the controls and console display
    #self.addObject(PlayerControlsWidget(**kwargs), handle='PlayerControls')
    self.addObject(FileControlButtonsWidget(**kwargs), handle='FileControlButtonLayout')

    # Connect the 'open' button to the open_file method
    self.connectSignal('open', self.readPlotFile)
    self.connectSignal('save', self.savePlotFile)
    self.connectSignal('reset', self.resetPlot)

    # Perform the setup for this object
    self.setup()

  ##
  # Method for reading a plot file and returning the information with a
  # plot widget.
  # @param file The file to read
  def readPlotFile(self, file):
    print >> sys.stderr, 'In readPlotFile, file=',file

  ##
  # Method for saving a plot file.
  # plot widget.
  # @param file The file to save plot information to.
  def savePlotFile(self, file):
    print >> sys.stderr, 'In savePlotFile, file=',file

  ##
  # Method for resetting a displayed plot to the beginning of time.
  # @param file The file to save plot information to.
  def resetPlot(self):
    print >> sys.stderr, 'In resetPlot'



#private:

  ##
  # Setup the execute menu
  #def _setupExecuteMenu(self, q_object):
  #  q_object.setTitle('Execute')

  #  # Add 'Run' menu item
  #  action = QtGui.QAction('&'+'Run', self)
  #  action.triggered.connect(self.callback('Run'))
  #  action.setShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_R))
  #  q_object.addAction(action)

  #  # Add 'Select' menu item
  #  #### I think we should do the same for 'Select' rather how it was done above

  ###
  ## Add the 'Select' menu action
  #def _setupSelectMenuAction(self, q_object):
  #  q_object.triggered.connect(self.callback('Select'))
  #  q_object.setShortcut(QtGui.QKeySequence(QtCore.Qt.CTRL + QtCore.Qt.Key_E))
