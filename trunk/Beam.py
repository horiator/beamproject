#!/usr/bin/python
# -*- coding: <<encoding>> -*-
#-------------------------------------------------------------------------------
#   DJ-application displaying currently playing song and upcoming tanda
# 
#-------------------------------------------------------------------------------

import wx, wx.html
import os, sys
from bin import HandleData, ParseSettings
from bin.Preferences import Preferences



##################################################
# HELP DIALOG
##################################################

class Help(wx.Dialog):
    def __init__(self, settings, *args, **kwargs):
        wx.Dialog.__init__(self, None, title="Help", size=(600,600))
        html 	= wxHTML(self)
	filename 	= 'docs/Help.html'
	dirname 	= os.getcwd()
	f 		= open(os.path.join(filename), 'r')
	page 	= f.read()
	f.close
        html.SetPage(page)
 
class wxHTML(wx.html.HtmlWindow):
     def OnLinkClicked(self, link):
         webbrowser.open(link.GetHref())




##################################################
# MAIN WINDOW - FRAME
##################################################
class Frame(wx.Frame):
    def __init__(self, title):
	
	# Size and position of the main window
        wx.Frame.__init__(self, None, title=title, pos=(150,150), size=(800,600))
	
	# Set Icon
	self.icon = 'icon.png'
	image = wx.Image(self.icon, wx.BITMAP_TYPE_PNG).ConvertToBitmap() 
	icon = wx.EmptyIcon() 
	icon.CopyFromBitmap(image) 
	self.SetIcon(icon)

	# Statusbar
        self.statusbar = self.CreateStatusBar(style=0)
	self.SetStatusText('Initializing...')

	# Setting up the menu.
        filemenu	= wx.Menu()
	Aboutmenu	= wx.Menu()
        menuPreferences 	= filemenu.Append(wx.ID_ANY, "&Preferences\tCtrl+P"," Configuration tool")
	menuFullScreen	= filemenu.Append(wx.ID_ANY, "&Fullscreen\tF11", "Set fullscreen")
        menuExit 	= filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")
        menuAbout	= Aboutmenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
	menuHelp	= Aboutmenu.Append(wx.ID_ANY, "&Help"," Getting started")

        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File") 	# Adding the "file menu" to the MenuBar
	menuBar.Append(Aboutmenu,"&About")	# Adding the "About menu" to the MenuBar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

        # Events.
        self.Bind(wx.EVT_MENU, self.OnPreferences, menuPreferences)
        self.Bind(wx.EVT_MENU, self.OnClose, menuExit)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
	self.Bind(wx.EVT_MENU, self.OnHelp, menuHelp)
	self.Bind(wx.EVT_MENU, self.fullScreen, menuFullScreen)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
	self.Bind(wx.EVT_LEFT_DCLICK, self.fullScreen)
	# This does not work in Linux - Try on Windows
	CtrlF	 = wx.NewId()
	CtrlP	 = wx.NewId()
	self.Bind(wx.EVT_MENU, self.fullScreen, id=CtrlP)
	self.Bind(wx.EVT_MENU, self.OnPreferences, id=CtrlP)
	self.AccelTable = wx.AcceleratorTable([(wx.ACCEL_CTRL, ord('F'), CtrlF)])
	self.AccelTable = wx.AcceleratorTable([(wx.ACCEL_CTRL, ord('P'), CtrlP)])
	self.SetAcceleratorTable(self.AccelTable)

	# Load default settings
	self.LoadSettings(self)	

	# Background	
	self.Bind(wx.EVT_SIZE, self.OnSize)
	self.Bind(wx.EVT_PAINT, self.OnPaint)
	self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)

	self.SetStatusText('Ready')
	

########################## END FRAME #########################

######
# LOAD SETTINGS
    def LoadSettings(self, openedFile):

	# Load from with settings parser
	self.SetStatusText('Loading settings...')
	self.filename = 'DefaultConfig.json' 
	self.dirname = os.getcwd()
	try:
		self.confFile = open(os.path.join(self.dirname, self.filename), 'r')
		ParseSettings.LoadConfig(self)
		self.confFile.close()
	except:
		print('Could not load DefaultConfig.json')

	# Start timer or Thread
	HandleData.Init(self)

	# Create an empty display line
	self.DisplayRow = []
	for i in range(0, len(self.MyDisplaySettings)): self.DisplayRow.append('')

	# Set background image
	self.backgroundImage = wx.Bitmap(str(os.path.join(self.dirname, self.BackgroundPath)))
	self.BackgroundImageWidth, self.BackgroundImageHeight = self.backgroundImage.GetSize()
	
	# Update
	self.updateData(self)

#
# UPDATE THE DATA
#
    def updateData(self, event):
	HandleData.GetData(self)
	if self.playbackStatus:
		self.SetStatusText(self.playbackStatus)
	self.Layout()
	self.Refresh()



#####################################################
# BACKGROUND
#
    def OnSize(self, size):
        self.Layout()
        self.Refresh()

    def OnEraseBackground(self, evt):
        pass

    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)
	self.Draw(dc)
#
# This is where the scaling of the image takes place
#
    def Draw(self, dc):
	# Get width and height of window
        cliWidth, cliHeight = self.GetClientSize()
        if not cliWidth or not cliHeight:
            return
        dc.Clear()
	
	# If the window is exactly the right size, draw and exit.
	if cliWidth == self.BackgroundImageWidth and cliHeight == self.BackgroundImageWidth:
		dc.DrawBitmap(self.BackgroundImage, 0, 0)
		return

	# Figure out how to scale the background image and position it
	aspectRatioWindow = float(cliHeight) / float(cliWidth)
	aspectRatioBackground = float(self.BackgroundImageHeight) / float(self.BackgroundImageWidth)
	result = self.backgroundImage
	
	if aspectRatioWindow >= aspectRatioBackground:
		# Window is too tall, scale to height
		Image = wx.ImageFromBitmap(self.backgroundImage)
		Image = Image.Scale(cliHeight*self.BackgroundImageWidth / self.BackgroundImageHeight, cliHeight, wx.IMAGE_QUALITY_NORMAL)
		result = wx.BitmapFromImage(Image)
	
	if aspectRatioWindow < aspectRatioBackground:
		# Window is too wide, scale to width
		Image = wx.ImageFromBitmap(self.backgroundImage)
		Image = Image.Scale(cliWidth, cliWidth*self.BackgroundImageHeight / self.BackgroundImageWidth, wx.IMAGE_QUALITY_NORMAL)
		result = wx.BitmapFromImage(Image)

	# Position the image and draw it
	resultWidth, resultHeight = result.GetSize()
        xPos = (cliWidth - resultWidth)/2
        yPos = (cliHeight - resultHeight)/2
        dc.DrawBitmap(result, xPos, yPos)
	
	#
	# DRAW TEXT
	#
	
	if self.playbackStatus in 'Playing':
		#Display what is playing
		DisplayLength = len(self.MyDisplaySettings)
	else:
		# Display the stopp-message
		DisplayLength = len(self.DisplayWhenStopped)
		

	for j in range(0, DisplayLength):
	
		if self.playbackStatus in 'Playing':
			#Display what is playing
			text 			= self.DisplayRow[j]
			Settings 		= self.MyDisplaySettings[j]
		else:
			# Display the stopp-message
			Settings 		= self.DisplayWhenStopped[j]
			text			= Settings['Field']
			
		# Get size and position
		Size 					= Settings['Size']*cliHeight/575
		HeightPosition 			= int(Settings['Position'][0]*cliHeight/100)	
		
		# Set font from settings
		dc.SetFont(wx.Font(Size, self.FontTypeDictionary[Settings['Font']], self.FontStyleDictionary[Settings['Style']], self.FontWeightDictionary[Settings['Weight']]))
		
		# Set font color, in the future, drawing a shadow ofsetted with the same text first might make a shadow!
		dc.SetTextForeground(eval(Settings['FontColor']))
		
		# Check if the text fits, cut it and add ...
		TextWidth, TextHeight 	= dc.GetTextExtent(text)	
		
		# Find length and position of text
		
		# Centered
		if Settings['Center'] == 'yes':
			while TextWidth > cliWidth:
				text = text[:-1]
				TextWidth, TextHeight = dc.GetTextExtent(text)
				if TextWidth < cliWidth:
					text = text[:-2]
					text = text + '...'
			TextWidth, TextHeight = dc.GetTextExtent(text)
			# Position
			WidthPosition = (cliWidth-TextWidth)/2
			
		# Not Centered
		else: 
			# Position
			WidthPosition = int(Settings['Position'][1]*cliWidth/100)
			while TextWidth > cliWidth-WidthPosition:
				text = text[:-1]
				TextWidth, TextHeight = dc.GetTextExtent(text)
				if TextWidth < cliWidth:
					text = text[:-2]
					text = text + '...'
			TextWidth, TextHeight = dc.GetTextExtent(text)

			
		# Draw the text
		dc.DrawText(text, WidthPosition,  HeightPosition)


#####################################################

#
# OPEN/IMPORT SETTINGS
#
    def OnPreferences(self, event):
	PreferencesDialog = Preferences(self)
        PrefDiag = PreferencesDialog.Show()

#
# FULLSCREEN
# 
    def fullScreen(self, event):
	self.ShowFullScreen(not self.IsFullScreen())
#
# CLOSE DIALOG
#
    def OnClose(self, event):
        dlg = wx.MessageDialog(self,
            "Do you really want to close this application?",
            "Confirm Exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
	    try:
	    	self.timer.Stop()
            	del self.timer
	    except:
		pass
	    self.Destroy()

#
# ABOUT DIALOG
# A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
#
    def OnAbout(self, event):
        description = """Beam is an advanced live media extractor for Unix, 
Windows and Mac operating system. Features include a
scalable display for TV or projector, customizable 
backgrounds and text, possibility to detect cortinas 
and display the next tanda.
"""
        licence = """Beam is free software; you can redistribute it and/or 
modify it under the terms of the GNU General Public 
License as published by the Free Software Foundation; 
either version 2 of the License, or (at your option) any
later version.

Beam is distributed in the hope that it will be useful, 
but WITHOUT ANY WARRANTY; without even the 
implied warranty of MERCHANTABILITY or FITNESS 
FOR A PARTICULAR PURPOSE.  See the GNU General 
Public License for more details. You should have 
received a copy of the GNU General Public License 
along with Beam; if not, write to the Free Software 
Foundation, Inc., 59 Temple Place, Suite 330, Boston, 
MA  02111-1307  USA"""

        info = wx.AboutDialogInfo()

        info.SetIcon(wx.Icon(self.icon, wx.BITMAP_TYPE_PNG))
        info.SetName('Beam')
        info.SetVersion('0.1')
        info.SetDescription(description)
        info.SetCopyright('(C) 2014 - 2015 Mikael Holber')
        info.SetWebSite('http://www.beam-project.com')
        info.SetLicence(licence)
        info.AddDeveloper('Mikael Holber and Horia Uifaleanu')

        wx.AboutBox(info)

#
# Open Help
#
    def OnHelp(self, event):
        help_dialog = Help(None, self)
        res = help_dialog.ShowModal()
        help_dialog.Destroy()



########################################################
# Start the main window
########################################################

#app = wx.App(redirect=True)    # Error messages go to popup window
app = wx.App(False)		# Error messages go to terminal, for debugging purposes
top = Frame("Beam")       # Sets the header of the window
top.Show()			# Show the window
app.MainLoop()			# Start the main loop which handles events
