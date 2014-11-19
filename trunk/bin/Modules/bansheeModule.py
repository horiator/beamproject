#!/usr/bin/python
# -*- coding: <<encoding>> -*-
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
#    Usage as function:
#       Artist, Album, Title, Genre, Comment, Composer, Year, playbackStatus = audaciousModule(MaxTandaLength)
#
#    Example:
#       Artist, Album, Title, Genre, Comment, Composer, Year, playbackStatus = audaciousModule.run(4)
#
#
#    Revision History:
#
#    18/10/2014 Version 1.0
#    	- Initial release
#
import imp
try:
    imp.find_module('dbus') #doesn't exist in Windows
    import dbus
except ImportError:
    found = False
    
from ID3 import *

def run(MaxTandaLength):
	bus = dbus.SessionBus()
	proxy = False

	Artist 		= []
	Album 		= []
	Title	 		= []
	Genre	 	= []
	Comment		= []
	Composer		= []
	Year			= []
	playbackStatus  = ''

	if banshee = bus.get_object("org.bansheeproject.Banshee", "/org/bansheeproject/Banshee/PlayerEngine")

	
	# If I cannot find previous, then set them to nothing
	Artist.append('')
	Album.append('')
	Title.append('')
	Genre.append('')
	Comment.append('')
	Composer.append('')
	Year.append('')

	# Retrieve current song
	if proxy != False:
		properties_manager = dbus.Interface(proxy, 'org.freedesktop.DBus.Properties')
		metadata = properties_manager.Get('org.mpris.MediaPlayer2.Player', 'Metadata')
		playbackStatus = properties_manager.Get('org.mpris.MediaPlayer2.Player', 'PlaybackStatus')
		if playbackStatus == 'Playing':
			for each in metadata:
				if each == "xesam:url":
					CurrentUrl = metadata = metadata[each]
					id3info = ID3(CurrentUrl.replace("file://", "").replace("%20"," "))
					Artist.append(id3info.artist)
					Album.append(id3info.album)
					Title.append(id3info.title)
					Genre.append(str(id3info.genre)) # Comes as a number, need table to transfer
					Comment.append(id3info.comment)
					Year.append(id3info.year)

	return Artist, Album, Title, Genre, Comment, Composer, Year, playbackStatus
