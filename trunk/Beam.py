#!/usr/bin/python
# -*- coding: <<encoding>> -*-
#-------------------------------------------------------------------------------
#   DJ-application displaying currently playing song and upcoming tanda
# 
#-------------------------------------------------------------------------------
#
#
#
import wx, wx.html
import os, sys

from bin.beamsettings import *
from bin.dialogs.beammainframe import beamMainFrame



#app = wx.App(redirect=True)    # Error messages go to popup window
app = wx.App(False)             # Error messages go to terminal, for debugging purposes


########################################################
# Load Settings (global object)
########################################################
confFile = open(os.path.join(os.getcwd(), beamSettings.defaultConfigFileName), 'r')
beamSettings.LoadConfig(confFile)
confFile.close()
print beamSettings.mainFrameTitle

########################################################
# Start the main window
########################################################
top = beamMainFrame()       # Creates the main frame
top.Show()                      # Shows the main frame

########################################################
# Start the timer used to update the displayed data
########################################################
if beamSettings._moduleSelected in ('Audacious', 'Rhythmbox','Itunes','Winamp','Clementine','Rhythmbox','Banshee','MediaMonkey'):
    # If the configuration have a timer on how often to update the data
    try:
        # There is not timer, so create and start it
        timer = wx.Timer(top)
        top.Bind(wx.EVT_TIMER, top.updateData, timer)
        timer.Start(beamSettings._updateTimer)
    except:
        # There is already a timer restart with new update timing
        timer.Stop()
        timer.Start(beamSettings._updateTimer)
if beamSettings._moduleSelected in ('Traktor'):
    # Other method, like read playlist from disk.
        pass

app.MainLoop()                  # Start the main loop which handles events
