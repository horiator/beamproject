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
import os, sys

##################################################
# Close DIALOG
##################################################

def ShowCloseDialog(self):
	
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
