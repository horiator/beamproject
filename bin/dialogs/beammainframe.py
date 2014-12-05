import wx, wx.html
import os, sys
import wx.lib.delayedresult


from bin.beamsettings import *
from bin import HandleData
from bin.Preferences import Preferences

from bin.dialogs.helpdialog import HelpDialog
from bin.dialogs import aboutdialog
from bin.dialogs import closedialog

STYLE = 0|wx.TRANSPARENT_WINDOW
##################################################
# MAIN WINDOW - FRAME
##################################################
class beamMainFrame(wx.Frame):
    def __init__(self, settings = None):
    # Size and position of the main window
        wx.Frame.__init__(self, None, title=beamSettings.mainFrameTitle, pos=(150,150), size=(800,600))

        self.SetDoubleBuffered(True)
        
    # Set Icon
        self.icon = 'icons/icon_square/icon_square_256px.png'
        image = wx.Image(self.icon, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        icon = wx.EmptyIcon()
        icon.CopyFromBitmap(image)
        self.SetIcon(icon)

    # faders
        self.timer1 = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.FadeoutOldImage, self.timer1)

        self.timer2 = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.FadeinNewImage, self.timer2)

    # Statusbar
        self.statusbar = self.CreateStatusBar(style=0)
        self.SetStatusText('Initializing...')

    # Setting up the menu.
        self.filemenu    = wx.Menu()
        self.Aboutmenu   = wx.Menu()
        self.menuPreferences = self.filemenu.Append(wx.ID_ANY, "&Preferences\tCtrl+P"," Configuration tool")
        self.menuFullScreen  = self.filemenu.Append(wx.ID_ANY, "&Fullscreen\tF11", "Set fullscreen")
        self.menuExit    = self.filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")
        self.menuAbout   = self.Aboutmenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
        self.menuHelp    = self.Aboutmenu.Append(wx.ID_ANY, "&Help"," Getting started")

    # Creating the menubar.
        self.menuBar = wx.MenuBar()
        self.menuBar.Append(self.filemenu,"&File")    # Adding the "file menu" to the MenuBar
        self.menuBar.Append(self.Aboutmenu,"&About")  # Adding the "About menu" to the MenuBar
        self.SetMenuBar(self.menuBar)  # Adding the MenuBar to the Frame content.

        # Events.
        self.Bind(wx.EVT_MENU, self.OnPreferences, self.menuPreferences)
        self.Bind(wx.EVT_MENU, self.OnClose, self.menuExit)
        self.Bind(wx.EVT_MENU, self.OnAbout, self.menuAbout)
        self.Bind(wx.EVT_MENU, self.OnHelp, self.menuHelp)
        self.Bind(wx.EVT_MENU, self.fullScreen, self.menuFullScreen)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.Bind(wx.EVT_LEFT_DCLICK, self.fullScreen)
    # This does not work in Linux - Try on Windows
        CtrlF    = wx.NewId()
        CtrlP    = wx.NewId()
        self.Bind(wx.EVT_MENU, self.fullScreen, id=CtrlP)
        self.Bind(wx.EVT_MENU, self.OnPreferences, id=CtrlP)
        self.AccelTable = wx.AcceleratorTable([(wx.ACCEL_CTRL, ord('F'), CtrlF)])
        self.AccelTable = wx.AcceleratorTable([(wx.ACCEL_CTRL, ord('P'), CtrlP)])
        self.SetAcceleratorTable(self.AccelTable)
    # Background
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.playbackStatus = ''
        self.SetStatusText('Ready')
        
        self.triggerChannelsAdjusted = True
        self.triggerBackgroundresize = True
        self.currentlyUpdating = False
        
        self.backgroundImage = wx.Bitmap(str(os.path.join(os.getcwd(), beamSettings._backgroundPath)))
        self.modifiedBitmap = self.backgroundImage
        self.BackgroundImageWidth, self.BackgroundImageHeight = self.backgroundImage.GetSize()


        self.applyCurrentSettings()
        self.updateData()
        



########################## END FRAME INITIALIZATION #########################

    def applyCurrentSettings(self):
    # Create an empty display line
        self.DisplayRow = []
        for i in range(0, len(beamSettings._myDisplaySettings)): self.DisplayRow.append('')

    # Set background image
        self.triggerBackgroundresize = True
        self.triggerChannelsAdjusted = True
        self.fadeBackground()

        self.Refresh()

#
# UPDATE THE DATA
#
    def updateData(self, event = wx.EVT_TIMER):
        if not self.currentlyUpdating:
            self.currentlyUpdating = True
            wx.lib.delayedresult.startWorker(self.getDataFinished, HandleData.GetData(self) )
        
    def getDataFinished(self, result):
        self.currentlyUpdating = False
        print "getData - workerfinished"
        if self.playbackStatus:
            self.SetStatusText(self.playbackStatus)
        self.Layout()
        self.Refresh()

#####################################################
# BACKGROUND resize and repaint
#
    def OnSize(self, size):
        self.triggerBackgroundresize = True
#        self.Layout()
        self.Refresh()
    def OnEraseBackground(self, evt):
        pass
    def OnPaint(self, event):
        dc = wx.BufferedPaintDC(self)
        self.Draw(dc)

    def drawBackgroundBitmap(self, dc):
        cliWidth, cliHeight = self.GetClientSize()
        if not cliWidth or not cliHeight:
            return

        if self.triggerBackgroundresize or self.triggerChannelsAdjusted:
            Image = wx.ImageFromBitmap(self.backgroundImage)           
            if self.triggerChannelsAdjusted:
                Image = Image.AdjustChannels(self.red, self.green, self.blue, 1.0)
                print self.red
            if self.triggerBackgroundresize:
                # Figure out how to scale the background image and position it
                aspectRatioWindow = float(cliHeight) / float(cliWidth)
                aspectRatioBackground = float(self.BackgroundImageHeight) / float(self.BackgroundImageWidth)
                if aspectRatioWindow >= aspectRatioBackground:
                    # Window is too tall, scale to height
                    Image = Image.Scale(cliHeight*self.BackgroundImageWidth / self.BackgroundImageHeight, cliHeight, wx.IMAGE_QUALITY_NORMAL)
                else:
                    # Window is too wide, scale to width
                    Image = Image.Scale(cliWidth, cliWidth*self.BackgroundImageHeight / self.BackgroundImageWidth, wx.IMAGE_QUALITY_NORMAL)
                    Image = Image.AdjustChannels(self.red, self.green, self.blue, 1.0)
            self.triggerBackgroundresize = False
            self.triggerChannelsAdjusted = False
            self.modifiedBitmap = wx.BitmapFromImage(Image)
        
        # Position the image and draw it
        resizedWidth, resizedHeight = self.modifiedBitmap.GetSize()
        self.xPosResized = (cliWidth - resizedWidth)/2
        self.yPosResized = (cliHeight - resizedHeight)/2
        dc.DrawBitmap(self.modifiedBitmap, self.xPosResized, self.yPosResized)

#
# This is where the scaling of the image takes place
#
    def Draw(self, dc):
    # Get width and height of window
        cliWidth, cliHeight = self.GetClientSize()
        if not cliWidth or not cliHeight:
            return
        dc.Clear()

        self.drawBackgroundBitmap(dc)
        # DRAW TEXT
        #

        if self.playbackStatus in 'Playing':
            #Display what is playing
            DisplayLength = len(beamSettings._myDisplaySettings)
        else:
            # Display the stopp-message
            DisplayLength = len(beamSettings._displayWhenStopped)
        for j in range(0, DisplayLength):
            if self.playbackStatus in 'Playing':
                #Display what is playing
                text = self.DisplayRow[j]
                Settings = beamSettings._myDisplaySettings[j]
            else:
                # Display the stopp-message
                Settings        = beamSettings._displayWhenStopped[j]
                text            = Settings['Field']
            # Get size and position
            Size = Settings['Size']*cliHeight/100
            HeightPosition = int(Settings['Position'][0]*cliHeight/100)
            # Set font from settings
            dc.SetFont(wx.Font(Size, beamSettings.FontTypeDictionary[Settings['Font']], beamSettings.FontStyleDictionary[Settings['Style']], beamSettings.FontWeightDictionary[Settings['Weight']]))

            # Set font color, in the future, drawing a shadow ofsetted with the same text first might make a shadow!
            dc.SetTextForeground(eval(Settings['FontColor']))

            # Check if the text fits, cut it and add ...
            TextWidth, TextHeight   = dc.GetTextExtent(text)
            # Find length and position of text

            # Centered
            if Settings['Center'] == 'yes':
                while TextWidth > cliWidth:
                    text = text.decode('utf-8')[:-1]
                    TextWidth, TextHeight = dc.GetTextExtent(text)
                    if TextWidth < cliWidth:
                        text = text.decode('utf-8')[:-1]
                        text = text + '...'
                TextWidth, TextHeight = dc.GetTextExtent(text)
            # Position
                WidthPosition = (cliWidth-TextWidth)/2

            # Not Centered
            else:
                # Position
                WidthPosition = int(Settings['Position'][1]*cliWidth/100)
                while TextWidth > cliWidth-WidthPosition:
                    text = text.decode('utf-8')[:-1]
                    TextWidth, TextHeight = dc.GetTextExtent(text)
                    if TextWidth < cliWidth-WidthPosition:
                        text = text.decode('utf-8')[:-1]
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

    # -----------------------------------------------------------------------------------




    def fadeBackground(self, fadeSpeed = 2):
        self.red = float(1.0)
        self.green = float(1.0)
        self.blue = float(1.0)
        self.delta = float(0.20)
        self.fadeSpeed = fadeSpeed


        # start the timer for the fadeout
        self.timer1.Start(self.fadeSpeed)
        print "FadeoutOldImage"

    def FadeoutOldImage(self, event):
        
        self.red -= 2 * self.delta
        self.green -= 2 * self.delta
        self.blue -= 2 * self.delta
        if self.red >= 0 and self.red <= 1:
            # refire the OnPaint event using self.Refresh
            self.Refresh()
            self.triggerChannelsAdjusted = True
        else:
            self.timer1.Stop()
            self.red = float(0.0)
            self.green = float(0.0)
            self.blue = float(0.0)
            self.timer2.Start(self.fadeSpeed)
            print "FadeinNewImage"
            triggerChannelsAdjusted = True
            triggerBackgroundresize = True
            self.backgroundImage = wx.Bitmap(str(os.path.join(os.getcwd(), beamSettings._backgroundPath)))
            self.BackgroundImageWidth, self.BackgroundImageHeight = self.backgroundImage.GetSize()


    # -----------------------------------------------------------------------------------
    def FadeinNewImage(self, event):
        
        self.red += self.delta
        self.green += self.delta
        self.blue += self.delta
        if self.red >= 0 and self.red <= 1:
            self.Refresh()
            self.triggerChannelsAdjusted = True
        else:
            self.timer2.Stop()
