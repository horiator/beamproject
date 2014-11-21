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
#       - Initial release
#

import wx, wx.html
import wx.lib.flatnotebook as fnb
import os

from bin.beamsettings import *


#
# Build main preferences Window
#

class Preferences(wx.Dialog):
    def __init__(self, parent):
        self.MainWindowParent = parent
        wx.Dialog.__init__(self, parent, title="Preferences", size=(400,400))

        # Build the panel
        self.panel = wx.Panel(self)
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.hbox = wx.BoxSizer(wx.HORIZONTAL)
        notebook  = fnb.FlatNotebook(self.panel, wx.ID_ANY,agwStyle=fnb.FNB_NODRAG|fnb.FNB_VC8|fnb.FNB_NO_NAV_BUTTONS|fnb.FNB_NO_X_BUTTON|fnb.FNB_NO_TAB_FOCUS)

        notebook.AddPage(self.BasicSettings(notebook), "Basic Settings")
        notebook.AddPage(self.LayoutSettings(notebook), "Layout")   
        notebook.AddPage(self.RulesSettings(notebook), "Cortinas and Rules")    

        self.button_ok = wx.Button(self.panel, label="Apply")
        self.button_cancel = wx.Button(self.panel, label="Close")
        self.button_ok.Bind(wx.EVT_BUTTON, self.onApply)
        self.button_cancel.Bind(wx.EVT_BUTTON, self.onClose)


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
        Mediaplayer = wx.StaticText(panel, -1, "Mediaplayer", (10,7))
        font = wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.BOLD) 
        Mediaplayer.SetFont(font)   
        wx.StaticText(panel, -1, "Select mediaplayer to display information from", (20,30))
        print beamSettings._currentModules
        self.Dropdown = wx.ComboBox(panel,value=beamSettings._moduleSelected, choices=beamSettings._currentModules, pos=(20,50))

        # Background image
        Background = wx.StaticText(panel, -1, "Background Image", (10,87))
        font = wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.BOLD) 
        Background.SetFont(font)    
        wx.StaticText(panel, -1, "Select background image (1920x1080 recommended)", (20,110))
        self.browse = wx.Button(panel, label="Browse", pos=(20,129))
        self.browse.Bind(wx.EVT_BUTTON, self.loadBackground)

        # Wait timer
        waittimer = wx.StaticText(panel, -1, "Settings", (10,167))
        font = wx.Font(11, wx.DEFAULT, wx.NORMAL, wx.BOLD) 
        waittimer.SetFont(font) 
        wx.StaticText(panel, -1, "Update timer in mSec (default 2000)", (20,190))
        self.TimerText = wx.TextCtrl(panel, -1, str(beamSettings._updateTimer), (20,210), (140,-1))

        # Tanda Length
        wx.StaticText(panel, -1, "Next tanda preview (number of songs, default 4)", (20,243))
        self.TandaLength = wx.TextCtrl(panel, -1, str(beamSettings._maxTandaLength), (20,263), (140,-1))

        return panel






#
# Second tab - Display
#

    def LayoutSettings(self, notebook):
        
        panel = wx.Panel(self)
        self.DisplayRows = []

        self.AddLayout  = wx.Button(panel, label="Add")
        self.DelLayout  = wx.Button(panel, label="Delete")
        self.EditLayout = wx.Button(panel, label="Edit")
        sizerbuttons    = wx.BoxSizer(wx.HORIZONTAL)
        sizerbuttons.Add(self.AddLayout, flag=wx.RIGHT | wx.TOP, border=10)
        sizerbuttons.Add(self.DelLayout, flag=wx.RIGHT | wx.TOP, border=10) 
        sizerbuttons.Add(self.EditLayout, flag=wx.RIGHT | wx.TOP, border=10)
        

        self.LayoutList = wx.ListBox(panel,-1, size=wx.DefaultSize, choices=[], style= wx.LB_NEEDED_SB)
        self.LayoutList.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.LayoutList.Bind(wx.EVT_LISTBOX_DCLICK, self.OnEditLayout)

        # Load data into table
        self.BuildLayoutList()
        
        self.AddLayout.Bind(wx.EVT_BUTTON, self.OnAddLayout)
        self.EditLayout.Bind(wx.EVT_BUTTON, self.OnEditLayout)
        self.DelLayout.Bind(wx.EVT_BUTTON, self.OnDelLayout)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.LayoutList, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)
        sizer.Add(sizerbuttons, flag=wx.LEFT | wx.BOTTOM | wx.TOP, border=10)
        panel.SetSizer(sizer)
        
        return panel


    def BuildLayoutList(self):
        self.DisplayRows = []
        for i in range(0, len(beamSettings._myDisplaySettings)): 
            Settings = beamSettings._myDisplaySettings[i]
            self.DisplayRows.append(Settings[u'Field'])
        self.LayoutList.Set(self.DisplayRows)

#
# Third tab - Rules
#

    def RulesSettings(self, notebook):
    
        panel = wx.Panel(self)
        
        self.RuleRows = []
        
        # Add buttons
        self.AddRule    = wx.Button(panel, label="Add")
        self.DelRule    = wx.Button(panel, label="Delete")
        self.EditRule   = wx.Button(panel, label="Edit")
        sizerbuttons    = wx.BoxSizer(wx.HORIZONTAL)
        sizerbuttons.Add(self.AddRule, flag=wx.RIGHT | wx.TOP, border=10)
        sizerbuttons.Add(self.DelRule, flag=wx.RIGHT | wx.TOP, border=10)   
        sizerbuttons.Add(self.EditRule, flag=wx.RIGHT | wx.TOP, border=10)
        
        self.AddRule.Bind(wx.EVT_BUTTON, self.OnAddRule)
        self.EditRule.Bind(wx.EVT_BUTTON, self.OnEditRule)
        self.DelRule.Bind(wx.EVT_BUTTON, self.OnDelRule)

        self.RuleList = wx.ListBox(panel,-1, size=wx.DefaultSize, choices=self.RuleRows, style= wx.LB_NEEDED_SB)
        self.RuleList.SetBackgroundColour(wx.Colour(255, 255, 255))
        self.RuleList.Bind(wx.EVT_LISTBOX_DCLICK, self.OnEditRule)

        # Load data into table
        self.BuildRuleList()
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.RuleList, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)
        sizer.Add(sizerbuttons, flag=wx.LEFT | wx.BOTTOM | wx.TOP, border=10)
        panel.SetSizer(sizer)
    
        return panel


    def BuildRuleList(self):
        self.RuleRows = []
        for i in range(0, len(beamSettings._rules)): 
            rule = beamSettings._rules[i]
            if rule[u'Type'] == "Set":
                self.RuleRows.append(str('Copy (Set) '+rule[u'Field1']+' to '+rule[u'Field2']))
            if rule[u'Type'] == "Cortina":
                if rule[u'Field2'] =="is":
                    self.RuleRows.append(str('Its a Cortina when: '+rule[u'Field1']+' is '+rule[u'Field3']))
                if rule[u'Field2'] =="is not":
                    self.RuleRows.append(str('Its a Cortina when: '+rule[u'Field1']+' is not '+rule[u'Field3']))
            if rule[u'Type'] == "Parse":
                self.RuleRows.append(str('Parse/split '+rule[u'Field1']+' containing '+rule[u'Field2']+' into '+rule[u'Field3']+' and '+rule[u'Field4']))
        self.RuleList.Set(self.RuleRows)


#
# Apply preferences
#
    def onApply(self, e):
        # Get Settings
        beamSettings._moduleSelected         = self.Dropdown.GetValue()  
        beamSettings._updateTimer        = int(self.TimerText.GetValue())
        beamSettings._maxTandaLength     =  int(self.TandaLength.GetValue())
            #try:
        confFile = open(os.path.join(os.getcwd(), beamSettings.defaultConfigFileName), 'w')
        beamSettings.SaveConfig(confFile)    
        confFile.close()
        
        # Apply current settings for the main frame
        self.MainWindowParent.applyCurrentSettings()

#
# Cancel preferences
#
    def onClose(self, e):
        self.Destroy()

    def GetSettings(self):
        return self.settings

    def loadBackground(self, event):
        openFileDialog = wx.FileDialog(self, "Open", "", "", 
                                       "Image files PNG (*.png)|*.png|Image files JPEG (*.jpg)|*.jpg", 
                                       wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
        if openFileDialog.ShowModal() == wx.ID_OK:        
            beamSettings._backgroundPath = openFileDialog.GetPath()
            openFileDialog.Destroy()



#
# LAYOUT BUTTONS
#
#

    def OnAddLayout(self, event):
        self.EditLayout = EditLayout(self, len(self.DisplayRows), "Add layout item")
        self.EditLayout.Show()

    def OnEditLayout(self, event):
        RowSelected = self.LayoutList.GetSelection()
        if RowSelected>-1:
            self.EditLayout = EditLayout(self, RowSelected, "Add layout item")
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
                beamsettings._myDisplaySettings.pop(RowSelected)
                self.BuildLayoutList()
#
# RULE BUTTONS
#
#
            
    def OnAddRule(self, event):
        self.EditRule = EditRule(self, self.RuleList.GetCount(), "Add rule")
        self.EditRule.Show()

        
    def OnEditRule(self, event):
        RowSelected = self.RuleList.GetSelection()
        if RowSelected>-1:
            self.EditRule = EditRule(self, RowSelected, "Edit rule")
            self.EditRule.Show()
       
    def OnDelRule(self, event):
        RowSelected = self.RuleList.GetSelection()
        if RowSelected>-1:
            LineToDelete = self.RuleList.GetString(RowSelected)
            dlg = wx.MessageDialog(self,
            "Do you really want to delete '"+LineToDelete+"' ?",
            "Confirm deletion", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
            result = dlg.ShowModal()
            dlg.Destroy()
            if result == wx.ID_OK:
                self.Rules.pop(RowSelected)
                self.BuildRuleList()



#
# LAYOUT WINDOW-CLASS
#
#

class EditLayout(wx.Dialog):
    def __init__(self, parent, RowSelected, mode):
        self.EditLayoutDialog   = wx.Dialog.__init__(self, parent, title=mode, size=(570,210))
        self.EditLayoutPanel        = wx.Panel(self)
        self.parent             = parent
        self.RowSelected        = RowSelected

        self.ButtonSaveLayout   = wx.Button(self.EditLayoutPanel, label="Save")
        self.ButtonCancelLayout     = wx.Button(self.EditLayoutPanel, label="Cancel")
        self.ButtonSaveLayout.Bind(wx.EVT_BUTTON, self.OnSaveLayoutItem)
        self.ButtonCancelLayout.Bind(wx.EVT_BUTTON, self.OnCancelLayoutItem)

        Fonts   = ["Decorative","Default","Modern","Roman","Script","Swiss","Teletype"]
        Weights     = ["Bold","Light","Normal"]
        Styles  = ["Italic","Normal","Slant"]
        
        # Check if it is a new line
        if self.RowSelected<len(beamSettings._myDisplaySettings):
            # Get the properties of the selected item
            self.Settings   = beamSettings._myDisplaySettings[self.RowSelected]
        else:
            # Create a new default setting
            self.Settings   = ({"Field": "Artist[1]", "Font": "Default","Style": "Normal", "Weight": "Bold", "Size": 20, "FontColor": "(255,255,255,255)", "HideControl": "NextTanda[1]", "Position": [50,50], "Center": "yes"})

        
        # Define fields
        self.LabelText          = wx.TextCtrl(self.EditLayoutPanel, size=(150,-1), value=self.Settings[u'Field'])
        self.FontDropdown       = wx.ComboBox(self.EditLayoutPanel,value=self.Settings[u'Font'], choices=Fonts)
        self.StyleDropdown      = wx.ComboBox(self.EditLayoutPanel,value=self.Settings[u'Style'], choices=Styles)
        self.WeightDropdown     = wx.ComboBox(self.EditLayoutPanel,value=self.Settings[u'Weight'], choices=Weights)
        self.SizeText           = wx.TextCtrl(self.EditLayoutPanel, value=str(self.Settings[u'Size']))
        self.ColorField         = wx.ColourPickerCtrl(self.EditLayoutPanel)
        self.HideText           = wx.TextCtrl(self.EditLayoutPanel, value=self.Settings[u'HideControl'])
        self.VerticalPos        = wx.TextCtrl(self.EditLayoutPanel, value=str(self.Settings[u'Position'][0]))
        self.HorizontalPos      = wx.TextCtrl(self.EditLayoutPanel, value=str(self.Settings[u'Position'][1]))
        #Checkbox
        self.CenterCheck        = wx.CheckBox(self.EditLayoutPanel, label="Center")
        self.CenterCheck.Bind(wx.EVT_CHECKBOX, self.DisableHorizontalBox)
        if self.Settings[u'Center']=="yes": 
            self.CenterCheck.SetValue(True)
            self.HorizontalPos.Enable(not self.CenterCheck.GetValue())
        # Set color
        self.ColorField.SetColour(eval(self.Settings[u'FontColor']))
        
        # Information area
        InfoGrid    =   wx.FlexGridSizer(4, 5, 5, 5)
        InfoGrid.AddMany ( [(wx.StaticText(self.EditLayoutPanel, label="Label"), 0, wx.EXPAND),
                        (wx.StaticText(self.EditLayoutPanel, label="Font"), 0, wx.EXPAND),
                        (wx.StaticText(self.EditLayoutPanel, label="Style"), 0, wx.EXPAND),
                        (wx.StaticText(self.EditLayoutPanel, label="Weight"), 0, wx.EXPAND),
                        (wx.StaticText(self.EditLayoutPanel, label="Size"), 0, wx.EXPAND),
                        (self.LabelText, 0, wx.EXPAND),
                        (self.FontDropdown, 0, wx.EXPAND),
                        (self.StyleDropdown, 0, wx.EXPAND),
                        (self.WeightDropdown, 0, wx.EXPAND),
                        (self.SizeText, 0, wx.EXPAND),
                        (wx.StaticText(self.EditLayoutPanel, label="Hide/Show"), 0, wx.EXPAND),
                        (wx.StaticText(self.EditLayoutPanel, label="Color"), 0, wx.EXPAND),
                        (wx.StaticText(self.EditLayoutPanel, label="Vertical"), 0, wx.EXPAND),
                        (wx.StaticText(self.EditLayoutPanel, label="Horizontal"), 0, wx.EXPAND),
                        (wx.StaticText(self.EditLayoutPanel, label=""), 0, wx.EXPAND),
                        (self.HideText, 0, wx.EXPAND),
                        (self.ColorField, 0, wx.EXPAND),
                        (self.VerticalPos, 0, wx.EXPAND),
                        (self.HorizontalPos, 0, wx.EXPAND),
                        (self.CenterCheck, 0, wx.EXPAND)
                        ])

        self.vboxLayout = wx.BoxSizer(wx.VERTICAL)
        self.hboxLayout = wx.BoxSizer(wx.HORIZONTAL)
        
        self.hboxLayout.Add((400, -1), 1, flag=wx.EXPAND | wx.ALIGN_RIGHT)
        self.hboxLayout.Add(self.ButtonSaveLayout, flag=wx.LEFT | wx.BOTTOM | wx.TOP, border=10)
        self.hboxLayout.Add(self.ButtonCancelLayout, flag=wx.LEFT | wx.BOTTOM | wx.TOP | wx.RIGHT, border=10)
        
        self.vboxLayout.Add(InfoGrid, flag=wx.LEFT | wx.BOTTOM | wx.TOP | wx.RIGHT, border=10)
        self.vboxLayout.Add(self.hboxLayout)

        self.EditLayoutPanel.SetSizer(self.vboxLayout)
        
    def DisableHorizontalBox(self, event):
        self.HorizontalPos.Enable(not self.CenterCheck.GetValue())
        
    def OnSaveLayoutItem(self, event):
        self.Settings[u'Field']         = self.LabelText.GetValue()
        self.Settings[u'Font']      = self.FontDropdown.GetValue()  
        self.Settings[u'Style']         = self.StyleDropdown.GetValue()
        self.Settings[u'Weight']        = self.WeightDropdown.GetValue()
        self.Settings[u'Size']      = int(self.SizeText.GetValue())
        self.Settings[u'HideControl']   = self.HideText.GetValue()
        self.Settings[u'FontColor']     = str(self.ColorField.GetColour())
        self.Settings[u'Position']  = [int(self.VerticalPos.GetValue()), int(self.HorizontalPos.GetValue())]
        if self.CenterCheck.GetValue():
            self.Settings[u'Center']    = 'yes'
        else:
            self.Settings[u'Center']    = 'no' 
        
        # Save item into dictionary
        if self.RowSelected+1 > len(beamSettings._myDisplaySettings):
            beamSettings._myDisplaySettings.append(self.Settings)
        else:
            beamSettings._myDisplaySettings[self.RowSelected] = self.Settings
        self.parent.BuildLayoutList()
        self.Destroy()
    
    def OnCancelLayoutItem(self, event):
        self.Destroy()


#
# Edit Rule class
#
#


class EditRule(wx.Dialog):
    def __init__(self, parent, RowSelected, mode):
        self.EditRuleDialog     = wx.Dialog.__init__(self, parent, title=mode, size=(470,210))
        self.EditRulePanel  = wx.Panel(self)
        self.parent             = parent
        self.RowSelected    = RowSelected
        self.mode           = mode

        self.ButtonSaveRule     = wx.Button(self.EditRulePanel, label="Save")
        self.ButtonCancelRule   = wx.Button(self.EditRulePanel, label="Cancel")
        self.ButtonSaveRule.Bind(wx.EVT_BUTTON, self.OnSaveRuleItem)
        self.ButtonCancelRule.Bind(wx.EVT_BUTTON, self.OnCancelRuleItem)
        self.InputFields    = ["Artist","Album","Title","Genre","Comment","Composer","Year"]
        self.OutputFields   = ["Artist","Album","Title","Genre","Comment","Composer","Year", "Singer"]

    # Check if it is a new line
        if self.RowSelected<len(beamSettings._rules):
            # Get the properties of the selected item
            self.Settings   = beamSettings._rules[self.RowSelected]
        else:
            # Create a new default setting
            self.Settings   = ({"Type": "Set", "Field1": "Comment","Field2": "Singer", "Active": "yes"})

        # Build the static elements
        self.InputID3Field      = wx.ComboBox(self.EditRulePanel,value=self.Settings[u'Field1'], choices=self.InputFields)
        self.RuleSelectDropdown     = wx.ComboBox(self.EditRulePanel,value=self.Settings[u'Type'], choices=['Set','Cortina','Parse'])
        self.RuleSelectDropdown.Bind(wx.EVT_COMBOBOX, self.ChangeRuleType)
        self.RuleOrder          = wx.TextCtrl(self.EditRulePanel, value=str(self.RowSelected+1))
        self.ActivateRule       = wx.CheckBox(self.EditRulePanel, label="Activate")
        
        if self.Settings[u'Active'] == "yes":
            self.ActivateRule.SetValue(True)
        
        # Dynamic fields (Changes depending on RuleSelectDropdown)
        self.DynamicFieldLabel1 = wx.StaticText(self.EditRulePanel, label="")
        self.DynamicFieldLabel2 = wx.StaticText(self.EditRulePanel, label="")
        self.TokenLabel         = wx.StaticText(self.EditRulePanel, label="Token")
        self.TokenField         = wx.TextCtrl(self.EditRulePanel, value="")
        
        self.sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        
        InfoGrid    =   wx.FlexGridSizer(4, 4, 5, 5)
        InfoGrid.AddMany ( [(wx.StaticText(self.EditRulePanel, label="Input ID3 tag"), 0, wx.EXPAND),
                        (wx.StaticText(self.EditRulePanel, label="Rule type"), 0, wx.EXPAND),
                        (self.DynamicFieldLabel1, 0, wx.EXPAND),
                        (self.DynamicFieldLabel2, 0, wx.EXPAND),
                        (self.InputID3Field, 0, wx.EXPAND),
                        (self.RuleSelectDropdown, 0, wx.EXPAND),
                        (self.sizer1, 0, wx.EXPAND),
                        (self.sizer2, 0, wx.EXPAND),
                        (wx.StaticText(self.EditRulePanel, label="Rule order"), 0, wx.EXPAND),
                        (self.TokenLabel, 0, wx.EXPAND),
                        (wx.StaticText(self.EditRulePanel, label=""), 0, wx.EXPAND),
                        (wx.StaticText(self.EditRulePanel, label=""), 0, wx.EXPAND),
                        (self.RuleOrder, 0, wx.EXPAND),
                        (self.TokenField, 0, wx.EXPAND)
                        ])
                        
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.hbox = wx.BoxSizer(wx.HORIZONTAL)
        
        self.EditRulePanel.SetSizer(self.vbox)
        
        self.hbox.Add((200, -1), 1, flag=wx.EXPAND | wx.ALIGN_RIGHT)
        self.hbox.Add(self.ActivateRule, flag=wx.LEFT | wx.TOP, border=13)
        self.hbox.Add(self.ButtonSaveRule, flag=wx.LEFT | wx.BOTTOM | wx.TOP, border=10)
        self.hbox.Add(self.ButtonCancelRule, flag=wx.LEFT | wx.BOTTOM | wx.TOP | wx.RIGHT, border=10)
        
        self.vbox.Add(InfoGrid, flag=wx.LEFT | wx.BOTTOM | wx.TOP | wx.RIGHT, border=10)
        self.vbox.Add(self.hbox)
        
        self.ChangeRuleType(self)
    
    
    def ChangeRuleType(self, event):
        RuleSelected = self.RuleSelectDropdown.GetValue()
        ###########################################
        if RuleSelected == 'Set':
            self.DynamicFieldLabel1.SetLabel('Output field')
            self.DynamicFieldLabel2.SetLabel('')
            # Remove fields that are not to be shown
            self.RemoveDynamicElements()        

            self.TokenLabel.Hide() 
            self.TokenField.Hide() 
            
            #Add correct fields
            self.OutputField1       = wx.ComboBox(self.EditRulePanel,value="Artist", choices=self.OutputFields)
            self.sizer1.Add(self.OutputField1)
            
            if self.Settings[u'Type'] == 'Set':
                self.OutputField1.SetStringSelection(self.Settings[u'Field2'])
            else:
                self.OutputField1.SetStringSelection("Artist")
                
        ########################################
        if RuleSelected == 'Parse':
            self.DynamicFieldLabel1.SetLabel('Output field 1')
            self.DynamicFieldLabel2.SetLabel('Output field 2')
            # Remove fields that are not to be shown
            self.RemoveDynamicElements()
            
            #Add correct fields
            self.OutputField1       = wx.ComboBox(self.EditRulePanel,value="Artist", choices=self.OutputFields)
            self.sizer1.Add(self.OutputField1)
            self.OutputField2       = wx.ComboBox(self.EditRulePanel,value="Artist", choices=self.OutputFields)
            self.sizer2.Add(self.OutputField2)

            if self.Settings[u'Type'] == 'Parse':
                self.OutputField1.SetStringSelection(self.Settings[u'Field3'])
                self.OutputField2.SetStringSelection(self.Settings[u'Field4'])
                self.TokenField.SetValue(self.Settings[u'Field2'])
            else: 
                self.OutputField1.SetStringSelection("Artist")
                self.OutputField2.SetStringSelection("Title")
                self.TokenField.SetValue("-")
            # Show Fields
            self.TokenLabel.Show() 
            self.TokenField.Show() 

        ##############################################      
        if RuleSelected == 'Cortina':
            self.DynamicFieldLabel1.SetLabel('is / is not')
            self.DynamicFieldLabel2.SetLabel('Value(s)')
            
            # Remove fields that are not to be shown
            self.RemoveDynamicElements()
            
            self.TokenLabel.Hide() 
            self.TokenField.Hide() 
            
            #Add correct fields
            self.IsIsNot    = wx.ComboBox(self.EditRulePanel,value="is", choices=["is", "is not"])
            self.sizer1.Add(self.IsIsNot)
            self.OutputField3 = wx.TextCtrl(self.EditRulePanel, value="", size=(165,-1))
            self.sizer2.Add(self.OutputField3)
            
            if self.Settings[u'Type'] == 'Cortina':
                self.IsIsNot.SetStringSelection(self.Settings[u'Field2'])
                self.OutputField3.SetValue(self.Settings[u'Field3'])
            else:
                self.IsIsNot.SetStringSelection("is")
                self.OutputField3.SetValue("")

        self.EditRulePanel.Layout()

    def RemoveDynamicElements(self):
        try:
            self.sizer1.Remove(self.OutputField1)
            self.OutputField1.Hide()
        except: pass
        try:
            self.sizer2.Remove(self.OutputField2)   
            self.OutputField2.Hide()
        except: pass
        try:
            self.sizer1.Remove(self.IsIsNot)
            self.IsIsNot.Hide()
        except: 
            pass
        try:
            self.sizer2.Remove(self.OutputField3)   
            self.OutputField3.Hide()
        except: 
            pass
            
            
    def OnSaveRuleItem(self, event):
        RuleOrderBox = int(self.RuleOrder.GetValue())-1
        RuleSelected = self.RuleSelectDropdown.GetValue()
        
        # Build NewRule
        NewRule = {}
        NewRule[u'Type']        = RuleSelected
        NewRule[u'Field1']      = self.InputID3Field.GetValue()
        if self.ActivateRule.GetValue():
            NewRule[u'Active']      = "yes"
        else:
            NewRule[u'Active']      = "no"
            
        if RuleSelected == 'Set':
            NewRule[u'Field2']      = self.OutputField1.GetValue()
        if RuleSelected == 'Parse':
            NewRule[u'Field2']      = self.TokenField.GetValue()
            NewRule[u'Field3']      = self.OutputField1.GetValue()
            NewRule[u'Field4']      = self.OutputField2.GetValue()
        if RuleSelected == 'Cortina':
            NewRule[u'Field2']      = self.IsIsNot.GetValue()
            NewRule[u'Field3']      = self.OutputField3.GetValue()
        
        # Decide where NewRule goes into the vector self.Settings
        if self.mode == "Add rule":
            if RuleOrderBox < self.RowSelected:
                beamSettings._rules.insert(RuleOrderBox, NewRule) #Insert in at position
            else:
                beamSettings._rules.append(NewRule) # Append in the end
        else: #Edit rule
            if RuleOrderBox == self.RowSelected:
                beamSettings._rules[RuleOrderBox] = NewRule # Overwrite
            else:
                beamSettings._rules.pop(self.RowSelected) #Move up and down in list
                beamSettings._rules.insert(RuleOrderBox, NewRule)
        self.parent.BuildRuleList()
        self.Destroy()

    def OnCancelRuleItem(self, event):
        self.Destroy()
