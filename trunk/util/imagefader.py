import wx
print wx.version()


STYLE = 0|wx.TRANSPARENT_WINDOW

# =======================================================================================
class ImageFader():
    red = float(1.0)
    green = float(1.0)
    blue = float(1.0)
    delta = float(0.01)

    # -----------------------------------------------------------------------------------
    def __init__(self, fadeSpeed=50):
                                
        self.timer1 = wx.Timer(self, wx.ID_ANY)
        self.Bind(wx.EVT_TIMER, self.FadeoutOldImage, self.timer1)

        self.timer2 = wx.Timer(self, wx.ID_ANY)
        self.Bind(wx.EVT_TIMER, self.FadeinNewImage, self.timer2)
        
        self.fadeSpeed = fadeSpeed

		oldImage = wx.Image(self.oldBackgroundImage, wx.BITMAP_TYPE_PNG)
		newImage = wx.Image(self.newBackgroundImage, wx.BITMAP_TYPE_PNG)
        
		# start the timer for the fadeout
        self.timer1.Start(self.fadeSpeed)
        print "FadeoutOldImage"

    # -----------------------------------------------------------------------------------
    def FadeoutOldImage(self, event):		
        self.red -= self.delta
        self.green -= self.delta
        self.blue -= self.delta
        if self.red >= 0 and self.red <= 1:
            # refire the OnPaint event using self.Refresh
		    self.backgroundImage = self.oldImage.AdjustChannels(self.red,self.green, self.blue, 1.0)
		    
		    # Set background image
		    self.backgroundImage = wx.Bitmap(str(os.path.join(os.getcwd(), beamSettings._backgroundPath)))
		    self.BackgroundImageWidth, self.BackgroundImageHeight = self.backgroundImage.GetSize()
		    self.triggerBackgroundresize = True

        else:
            self.timer1.Stop()
			self.timer2.Start(self.fadeSpeed)
	        print "FadeinNewImage"
 
    # -----------------------------------------------------------------------------------
    def FadeinNewImage(self, event):
        self.red += self.delta
        self.green += self.delta
        self.blue += self.delta
        if self.red >= 0 and self.red <= 1:
            # refire the OnPaint event using self.Refresh
		    self.backgroundImage = self.image.AdjustChannels(self.red,self.green, self.blue, 1.0)
		    
		    # Set background image
		    self.backgroundImage = wx.Bitmap(str(os.path.join(os.getcwd(), beamSettings._backgroundPath)))
		    self.BackgroundImageWidth, self.BackgroundImageHeight = self.backgroundImage.GetSize()
		    self.triggerBackgroundresize = True
        else:
            self.timer2.Stop()


app = wx.App(False)
frm = wx.Frame(None)
pnl = ImageFader(frm, wx.DefaultPosition, wx.DefaultSize, "fade.png")
frm.Show()
app.MainLoop()

