#    Copyright (C) 2014 Mikael Holber http://mywebsite.com
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
#    22/10/2014 Version 1.0
#    	- Initial release
#

import wx, wx.html
import wx.lib.flatnotebook as fnb
from bin import ParseSettings
import os


#
# Build main preferences Window
#

class Preferences(wx.Dialog):
    def __init__(self, settings, *args, **kwargs):
        wx.Dialog.__init__(self, None, title="Preferences", size=(400,400))
	
	# Load the global variables with the file-reader
	self.filename = 'DefaultConfig.json' 
        self.dirname = os.getcwd()
	try:
        	self.confFile = open(os.path.join(self.dirname, self.filename), 'r')
	    	# Go to loadSettings and read settings
		ParseSettings.LoadConfig(self)
        	self.confFile.close()
	except:
		print "Could not load settings file DefaultConfig.json"

	# Build the panel
        self.panel = wx.Panel(self)
	self.vbox = wx.BoxSizer(wx.VERTICAL)
	self.hbox = wx.BoxSizer(wx.HORIZONTAL)
        notebook  = fnb.FlatNotebook(self.panel, wx.ID_ANY,agwStyle=fnb.FNB_NODRAG|fnb.FNB_VC8|fnb.FNB_NO_NAV_BUTTONS|fnb.FNB_NO_X_BUTTON|fnb.FNB_NO_TAB_FOCUS)

        notebook.AddPage(self.BasicSettings(notebook), "Basic Settings")
	notebook.AddPage(self.LayoutSettings(notebook), "Layout")	
	notebook.AddPage(self.RulesSettings(notebook), "Cortinas and Rules")	

        self.button_ok = wx.Button(self.panel, label="Save")
        self.button_cancel = wx.Button(self.panel, label="Cancel")
        self.button_ok.Bind(wx.EVT_BUTTON, self.onOk)
        self.button_cancel.Bind(wx.EVT_BUTTON, self.onCancel)


	self.vbox.Add(notebook, 1, wx.ALL | wx.EXPAND)
	self.hbox.Add((200, -1), 1, flag=wx.EXPAND | wx.ALIGN_RIGHT)
        self.hbox.Add(self.button_ok, flag=wx.LEFT | wx.BOTTOM | wx.TOP, border=10)
        self.hbox.Add(self.button_cancel, flag=wx.LEFT | wx.BOTTOM | wx.TOP | wx.RIGHT, border=10)
	self.vbox.Add(self.hbox)

        self.panel.SetSizerAndFit(self.vbox)












#
# First tab - Basic Settings
#
    def BasicSettings(self, notebook):
	
	panel = wx.Panel(notebook)

	# Module dropdown
	Mediaplayer = wx.StaticText(panel, -1, "Mediaplayer", (10,10))
	font = wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.BOLD) 
        Mediaplayer.SetFont(font) 	
	wx.StaticText(panel, -1, "Select mediaplayer to display information from", (20,40))
	self.Dropdown = wx.ComboBox(panel,value=self.ModuleSelected, choices=self.AllModules, pos=(20,60))

	# Background image
	Background = wx.StaticText(panel, -1, "Background Image", (10,100))
	font = wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.BOLD) 
        Background.SetFont(font)	
	wx.StaticText(panel, -1, "Select background image (1920x1080 recommended)", (20,130))
	self.browse = wx.Button(panel, label="Browse", pos=(20,149))
	self.browse.Bind(wx.EVT_BUTTON, self.loadBackground)

	# Wait timer
	waittimer = wx.StaticText(panel, -1, "Background Image", (10,190))
	font = wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.BOLD) 
        waittimer.SetFont(font)	
	wx.StaticText(panel, -1, "Update timer in mSec (default 2000)", (20,220))
	self.TimerText = wx.TextCtrl(panel, -1, str(self.updateTimer), (20,240), (140,-1))

        return panel






#
# Second tab - Display
#

    def LayoutSettings(self, notebook):
        
	panel = wx.Panel(self)
	self.DisplayRows = []

	# Load data into table
	for i in range(0, len(self.MyDisplaySettings)): 
		Settings = self.MyDisplaySettings[i]
		self.DisplayRows.append(Settings[u'Field'])
	
	self.AddLayout	= wx.Button(panel, label="Add")
	self.DelLayout 	= wx.Button(panel, label="Delete")
	self.EditLayout	= wx.Button(panel, label="Edit")
	sizerbuttons	= wx.BoxSizer(wx.HORIZONTAL)
        sizerbuttons.Add(self.AddLayout, flag=wx.RIGHT | wx.TOP, border=10)
        sizerbuttons.Add(self.DelLayout, flag=wx.RIGHT | wx.TOP, border=10)	
	sizerbuttons.Add(self.EditLayout, flag=wx.RIGHT | wx.TOP, border=10)

	self.LayoutList = wx.ListBox(panel,-1, size=wx.DefaultSize, choices=self.DisplayRows, style= wx.LB_NEEDED_SB)
        self.LayoutList.SetBackgroundColour(wx.Colour(255, 255, 255))
	
	self.AddLayout.Bind(wx.EVT_BUTTON, self.OnAddLayout)
	self.EditLayout.Bind(wx.EVT_BUTTON, self.OnEditLayout)
	self.DelLayout.Bind(wx.EVT_BUTTON, self.OnDelLayout)
	
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.LayoutList, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)
	sizer.Add(sizerbuttons, flag=wx.LEFT | wx.BOTTOM | wx.TOP, border=10)
	panel.SetSizer(sizer)
	
        return panel





#
# Third tab - Rules
#

    def RulesSettings(self, notebook):
	
	panel = wx.Panel(self)
	
	self.RuleRows = []
	
	# Load data into table
	for i in range(0, len(self.Rules)): 
		rule = self.Rules[i]
		if rule[u'Type'] == "Set":
			self.RuleRows.append(str('Copy (Set) '+rule[u'Field1']+' to '+rule[u'Field1']))
		if rule[u'Type'] == "Cortina":
			if rule[u'Field2'] =="is":
				self.RuleRows.append(str('Its a Cortina when: '+rule[u'Field1']+' is '+rule[u'Field3']))
			if rule[u'Field2'] =="isNot":
				self.RuleRows.append(str('Its a Cortina when: '+rule[u'Field1']+' is not '+rule[u'Field3']))
		if rule[u'Type'] == "Parse":
			self.RuleRows.append(str('Parse/split '+rule[u'Field1']+' containing '+rule[u'Field2']+' into '+rule[u'Field3']+' and '+rule[u'Field4']))
	
	# Add buttons
	self.AddRule 	= wx.Button(panel, label="Add")
	self.DelRule	= wx.Button(panel, label="Delete")
	self.EditRule	= wx.Button(panel, label="Edit")
	sizerbuttons	= wx.BoxSizer(wx.HORIZONTAL)
        sizerbuttons.Add(self.AddRule, flag=wx.RIGHT | wx.TOP, border=10)
        sizerbuttons.Add(self.DelRule, flag=wx.RIGHT | wx.TOP, border=10)	
	sizerbuttons.Add(self.EditRule, flag=wx.RIGHT | wx.TOP, border=10)
	
	self.AddRule.Bind(wx.EVT_BUTTON, self.OnAddRule)
	self.EditRule.Bind(wx.EVT_BUTTON, self.OnEditRule)
	self.DelRule.Bind(wx.EVT_BUTTON, self.OnDelRule)

	self.RuleList = wx.ListBox(panel,-1, size=wx.DefaultSize, choices=self.RuleRows, style= wx.LB_NEEDED_SB)
        self.RuleList.SetBackgroundColour(wx.Colour(255, 255, 255))
	
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.RuleList, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)
	sizer.Add(sizerbuttons, flag=wx.LEFT | wx.BOTTOM | wx.TOP, border=10)
	panel.SetSizer(sizer)
	
        return panel


#
# Apply preferences
#
    def onOk(self, e):
        # Get Settings
	self.ModuleSelected = self.Dropdown.GetValue()	
	# Write Settings
	try:
		self.updateTimer = int(self.TimerText.GetValue())
		self.filename = 'DefaultConfig.json' 
		self.dirname = os.getcwd()
		try:
			self.confFile = open(os.path.join(self.dirname, self.filename), 'w')
			ParseSettings.SaveConfig(self)	
			self.confFile.close()
		except:
			print 'Error: Could not write to DefaultConfig.json'
	        self.EndModal(wx.ID_OK)
	except:
		print 'Error: Update timer contains letters.'

#
# Cancel preferences
#
    def onCancel(self, e):
        self.EndModal(wx.ID_CANCEL)
	
	


    def GetSettings(self):
        return self.settings

    def loadBackground(self, event):
        openFileDialog = wx.FileDialog(self, "Open", "", "", 
                                       "Image files (*.png)|*.png", 
                                       wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
	if openFileDialog.ShowModal() == wx.ID_OK:        
		self.BackgroundPath = openFileDialog.GetPath()
        openFileDialog.Destroy()



#
# LAYOUT BUTTONS
#
#

    def OnAddLayout(self, event):
	print 'Add Layout'
		
    def OnEditLayout(self, event):
	RowSelected = self.LayoutList.GetSelection()
	if RowSelected>-1:
		print 'Edit Layout'
		print RowSelected
		EditDialog = wx.Dialog(self, None, title="Add/Edit", size=(200,400))


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
			print 'Deleted'
			#Code to delete goes here
	
	
	
	
	
    def OnAddRule(self, event):
	   print 'Add Rule'

		
    def OnEditRule(self, event):
	RowSelected = self.RuleList.GetSelection()
	if RowSelected>-1:
		print RowSelected
		print 'Edit Rule'
	   
    def OnDelRule(self, event):
	   print 'Del Rule'
	
