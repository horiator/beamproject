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
# About DIALOG
##################################################

def ShowAboutDialog(self):
	
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
	info.AddArtist('Artwork by Andreea Vlad - www.andreeavlad.com')
	wx.AboutBox(info)
