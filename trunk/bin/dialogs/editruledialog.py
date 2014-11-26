import wx, wx.html
import os

from bin.beamsettings import *

#
# Edit Rule class
#
#
class EditRuleDialog(wx.Dialog):
    def __init__(self, parent, RowSelected, mode):
        self.EditRuleDialog     = wx.Dialog.__init__(self, parent, title=mode, size=(600,210))
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
