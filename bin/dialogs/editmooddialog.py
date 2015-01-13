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
    def __init__(self, parent):
        self.MainWindowParent = parent
        wx.Dialog.__init__(self, parent, title="Edit mood layout", size=(400,400))

        # Build the panel
        self.panel = wx.Panel(self)
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.button_ok = wx.Button(self.panel, label="Save")
        self.button_cancel = wx.Button(self.panel, label="Close")
        self.button_ok.Bind(wx.EVT_BUTTON, self.onSave)
        self.button_cancel.Bind(wx.EVT_BUTTON, self.onClose)


        self.vbox.Add(self.LayoutSettings(), 1, wx.ALL | wx.EXPAND)
        self.hbox.Add((200, -1), 1, flag=wx.EXPAND | wx.ALIGN_RIGHT)
        self.hbox.Add(self.button_ok, flag=wx.LEFT | wx.BOTTOM | wx.TOP, border=10)
        self.hbox.Add(self.button_cancel, flag=wx.LEFT | wx.BOTTOM | wx.TOP | wx.RIGHT, border=10)
        self.vbox.Add(self.hbox)

        self.panel.SetSizerAndFit(self.vbox)


    def LayoutSettings(self):

        panel = wx.Panel(self)
        self.DisplayRows = []
        LayoutText = wx.StaticText(panel, -1, "Mood layout")
        font = wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        LayoutText.SetFont(font)

        BackgroundHeader = wx.StaticText(panel, -1, "Mood Background")
        BackgroundHeader.SetFont(font)

        self.AddLayout  = wx.Button(panel, label="Add")
        self.DelLayout  = wx.Button(panel, label="Delete")
        self.EditLayout = wx.Button(panel, label="Edit")
        self.MoodBackground = wx.Button(panel, label="Browse")
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
        sizer.Add(LayoutText, flag=wx.LEFT | wx.TOP, border=5)
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