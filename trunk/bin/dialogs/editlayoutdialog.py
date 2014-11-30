import wx, wx.html
import os

from bin.beamsettings import *

#
# LAYOUT WINDOW-CLASS
#
#
class EditLayoutDialog(wx.Dialog):
    def __init__(self, parent, RowSelected, mode):
        self.EditLayoutDialog   = wx.Dialog.__init__(self, parent, title=mode, size=(840,210))
        self.EditLayoutPanel    = wx.Panel(self)
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
