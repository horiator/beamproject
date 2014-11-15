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
from bin import HandleData, ParseSettings
from bin.Preferences import Preferences

from bin.dialogs.helpdialog import HelpDialog
from bin.dialogs import aboutdialog
from bin.dialogs import closedialog

##################################################
# MAIN WINDOW - FRAME
##################################################
class Frame(wx.Frame):
    def __init__(self, title):
	
	# Size and position of the main window
        wx.Frame.__init__(self, None, title=title, pos=(150,150), size=(800,600))
	
	# Set Icon
	self.icon = 'icons/icon_square/icon_square_256px.png'
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
	self.confFile = open(os.path.join(self.dirname, self.filename), 'r')
	ParseSettings.LoadConfig(self)
	self.confFile.close()


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
		Size 					= Settings['Size']*cliHeight/100
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
# Show 'Close dialog
#
    def OnClose(self, event):
        closedialog.ShowCloseDialog(self)
        
    def OnClose1(self, event):
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
# Show 'About Dialog'
#
    def OnAbout(self, event):
        aboutdialog.ShowAboutDialog(self)
        
#
# Show 'Help'
#
    def OnHelp(self, event):
        help_dialog = HelpDialog(None, self)
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
