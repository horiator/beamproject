#!/usr/bin/env python
# -*- coding: utf-8 -*-
#    Copyright (C) 2014 Mikael Holber http://http://www.beam-project.com
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, write to the Free Software
#    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#    or download it from http://www.gnu.org/licenses/gpl.txt
#
#
#    Revision History:
#
#    XX/XX/2014 Version 1.0
#       - Initial release
#
# This Python file uses the following encoding: utf-8

import wx
import os

from bin.beamsettings import *

#
# Build Mood Layout Window
#

class EditMood(wx.Dialog):
    def __init__(self, parent, RowSelected, mode):
        self.MainWindowParent = parent
        wx.Dialog.__init__(self, parent, title=mode, size=(400,500))
        self.RowSelected = RowSelected
        self.Settings = {}
        
        # Define choices
        self.Fields   = ["%Artist","%Album","%Title","%Genre","%Comment","%Composer","%Year", "%AlbumArtist", "%Performer", "%Singer","%IsCortina"]
        # Get item
        if self.RowSelected<len(beamSettings._moods):
            # Get the properties of the selected item
            self.Settings   = beamSettings._moods[self.RowSelected]
        else:
            # Create a new default setting
            self.Settings   = ({"Active": "yes", "Field3": "","Field2": "is","Field1": "%Artist",
                               "Type": "Mood", "Name": "Not running Mood",
                               "Background": "resources/backgrounds/bg1920x1080px_darkGreen.jpg",
                               "PlayState": "PlayerNotRunning",
                               "Display": [{"Active": "yes", "Style": "Italic","Center": "yes",
                                           "Weight": "Bold", "HideControl": "", "Row": 1,
                                           "Field": "Beam", "FontColor": "(255,255,255,255)",
                                           "Position": [30,0],"Font": "Roman","Size": 10},
                                           {"Active": "yes","Style": "Italic","Center": "yes",
                                           "Weight": "Bold","Row": 2,"Field": "Me Up Scotty",
                                           "HideControl": "", "FontColor": "(255,255,255,255)",
                                           "Position": [50,0],"Font": "Roman","Size": 8}]})

        # Build the panel
        self.panel = wx.Panel(self)
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.hbox = wx.BoxSizer(wx.HORIZONTAL)

        # Save/Close-buttons
        self.button_ok = wx.Button(self.panel, label="Save")
        self.button_cancel = wx.Button(self.panel, label="Close")
        self.button_ok.Bind(wx.EVT_BUTTON, self.onSave)
        self.button_cancel.Bind(wx.EVT_BUTTON, self.onClose)
        self.hbox.Add((200, -1), 1, flag=wx.EXPAND | wx.ALIGN_RIGHT)
        self.hbox.Add(self.button_ok, flag=wx.LEFT | wx.BOTTOM | wx.TOP, border=10)
        self.hbox.Add(self.button_cancel, flag=wx.LEFT | wx.BOTTOM | wx.TOP | wx.RIGHT, border=10)
        
        # Description Settings
        PropertiesText = wx.StaticText(self.panel, -1, "Properties")
        font = wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        PropertiesText.SetFont(font)
        self.vbox.Add(PropertiesText, border=10)
        
        # Add settings
        self.vbox.Add(self.MoodSettings(), 1, wx.ALL | wx.EXPAND, border=10)

        # Description Layout and background
        LayoutText = wx.StaticText(self.panel, -1, "Layout")
        font = wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        LayoutText.SetFont(font)
        
        BackgroundText = wx.StaticText(self.panel, -1, "Select background image (1920x1080 recommended)", (20,110))
        self.MoodBackground = wx.Button(self.panel, label="Browse")
        descriptionSizer = wx.BoxSizer(wx.VERTICAL)
        descriptionSizer.Add(LayoutText)
        descriptionSizer.Add(BackgroundText)
        descriptionSizer.Add(self.MoodBackground)
        self.vbox.Add(descriptionSizer, border=10)

        # Add Layout
        self.vbox.Add(self.LayoutSettings(), 1, wx.ALL | wx.EXPAND)

        # Set sizers
        self.vbox.Add(self.hbox)
        self.panel.SetSizerAndFit(self.vbox)
    
    
#
# Mood settings
#
    def MoodSettings(self):

        # Create the fields
        
        self.InputID3Field = wx.ComboBox(self.panel, size=(120,-1), value=self.Settings[u'Field1'], choices=self.Fields, style=wx.CB_READONLY)
        self.IsIsNot       = wx.ComboBox(self.panel,value="is", choices=["is", "is not"], style=wx.CB_READONLY)
        self.MoodOrder     = wx.TextCtrl(self.panel, value=str(self.RowSelected+1))
        self.OutputField   = wx.TextCtrl(self.panel, value="", size=(130,-1))
        self.MoodNameField = wx.TextCtrl(self.panel, value="", size=(120,-1))
        self.MoodState     = wx.ComboBox(self.panel,value="", choices=["Playing", "Paused","Stopped","PlayerNotRunning"], size=(120,-1), style=wx.CB_READONLY)

        InfoGrid    =   wx.FlexGridSizer(6, 3, 5, 5)
        InfoGrid.AddMany ( [(wx.StaticText(self.panel, label="Name"), 0, wx.EXPAND),
                        (wx.StaticText(self.panel, label="Mood state"), 0, wx.EXPAND),
                        (wx.StaticText(self.panel, label="Mood order"), 0, wx.EXPAND),
                        (self.MoodNameField, 0, wx.EXPAND),
                        (self.MoodState, 0, wx.EXPAND),
                        (self.MoodOrder, 0, wx.EXPAND),
                        (wx.StaticText(self.panel, label="Input field"), 0, wx.EXPAND),
                        (wx.StaticText(self.panel, label="is/is not"), 0, wx.EXPAND),
                        (wx.StaticText(self.panel, label="Output field"), 0, wx.EXPAND),
                        (self.InputID3Field, 0, wx.EXPAND),
                        (self.IsIsNot, 0, wx.EXPAND),
                        (self.OutputField, 0, wx.EXPAND)
                        ])
        
        return InfoGrid

#
# Mood layout
#
    def LayoutSettings(self):

        panel = wx.Panel(self)
        self.DisplayRows = []

        self.AddLayout  = wx.Button(panel, label="Add")
        self.DelLayout  = wx.Button(panel, label="Delete")
        self.EditLayout = wx.Button(panel, label="Edit")

        sizerbuttons    = wx.BoxSizer(wx.HORIZONTAL)
        sizerbuttons.Add(self.AddLayout, flag=wx.RIGHT | wx.TOP, border=10)
        sizerbuttons.Add(self.DelLayout, flag=wx.RIGHT | wx.TOP, border=10)
        sizerbuttons.Add(self.EditLayout, flag=wx.RIGHT | wx.TOP, border=10)

        self.LayoutList = wx.CheckListBox(panel,-1, size=wx.DefaultSize, choices=[], style= wx.LB_NEEDED_SB)
        self.LayoutList.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.LayoutList.Bind(wx.EVT_LISTBOX_DCLICK, self.OnEditLayout)
        self.LayoutList.Bind(wx.EVT_CHECKLISTBOX, self.OnCheckLayout)

        # Load data into table
        self.BuildLayoutList()

        self.AddLayout.Bind(wx.EVT_BUTTON, self.OnAddLayout)
        self.EditLayout.Bind(wx.EVT_BUTTON, self.OnEditLayout)
        self.DelLayout.Bind(wx.EVT_BUTTON, self.OnDelLayout)
        self.MoodBackground.Bind(wx.EVT_BUTTON, self.BrowseMoodBackground)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.LayoutList, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)
        sizer.Add(sizerbuttons, flag=wx.LEFT | wx.BOTTOM | wx.TOP, border=10)
        panel.SetSizer(sizer)

        return panel

    def BuildLayoutList(self):
        self.DisplayRows = []
        for i in range(0, len(beamSettings._DefaultDisplaySettings)):
            Settings = beamSettings._DefaultDisplaySettings[i]
            self.DisplayRows.append(Settings[u'Field'])
        self.LayoutList.Set(self.DisplayRows)


#
# LAYOUT BUTTONS
#
#
    def OnAddLayout(self, event):
        self.EditLayout = EditLayoutDialog(self, len(self.DisplayRows), "Add layout item")
        self.EditLayout.Show()

    def OnEditLayout(self, event):
        RowSelected = self.LayoutList.GetSelection()
        if RowSelected>-1:
            self.EditLayout = EditLayoutDialog(self, RowSelected, "Add layout item")
            self.EditLayout.Show()

    def OnDelLayout(self, event):
        RowSelected = self.LayoutList.GetSelection()
        if RowSelected>-1:
            LineToDelete = self.LayoutList.GetString(RowSelected)
            dlg = wx.MessageDialog(self,
            "Do you really want to delete '"+LineToDelete+"' ?",
            "Confirm deletion", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
            result = dlg.ShowModal()
            dlg.Destroy()
            if result == wx.ID_OK:
                beamSettings._DefaultDisplaySettings.pop(RowSelected)
                self.BuildLayoutList()

#
# Save mood layout
#
    def onSave(self, e):
        # Get Settings
        #beamSettings._moduleSelected     = self.Dropdown.GetValue()
        #beamSettings._updateTimer        = int(self.TimerText.GetValue())
        #beamSettings._maxTandaLength     =  int(self.TandaLength.GetValue())
        #beamSettings.SaveConfig(beamSettings.defaultConfigFileName)
        self.Destroy()

#
# Cancel mood layout
#
    def onClose(self, e):
        self.Destroy()

    def OnCheckLayout(self, event):
        for i in range(0, len(beamSettings._DefaultDisplaySettings)):
            layout = beamSettings._DefaultDisplaySettings[i]
            if self.LayoutList.IsChecked(i):
                layout[u'Active'] = "yes"
            else:
                layout[u'Active'] = "no"
        self.BuildLayoutList()

    def BrowseMoodBackground(self, event):
        print "Browse for Mood Background"