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

	Artist 		= []
	Album 		= []
	Title	 		= []
	Genre	 	= []
	Comment	= []
	Composer	= []
	Year			= []
	playbackStatus  = ''

	bus = dbus.SessionBus()
	player = bus.get_object('org.mpris.clementine', '/Player')
	tracklist = bus.get_object('org.mpris.clementine', '/TrackList')
	
	
	#Declare our position
	currentsong	= tracklist.GetCurrentTrack()
	listlength		= tracklist.GetLength()
	print currentsong
	print listlength

	# Extract previous song
	if currentsong == 0:
		searchsong = currentsong # Start on the current song
	else:
		searchsong = currentsong-1 # Start on previous song
		
	while searchsong < currentsong+MaxTandaLength+2 and listlength-1:
		#try:
			Track = tracklist.GetMetadata(searchsong)
			try:
				Artist.append((Track[u'artist'].encode('utf-8')).encode('cp1250'))
			except:
				Artist.append("")
			Album.append(Track[u'album'].encode('cp1250'))
			Title.append(Track[u'title'].encode('cp1250'))
			Genre.append(Track[u'genre'].encode('cp1250'))
			Comment.append(Track[u'comment'].encode('cp1250'))
			Composer.append("")
			Year.append(Track[u'year'])
			searchsong = searchsong+1
		#except:
		#		break
				
	
	
	
	return Artist, Album, Title, Genre, Comment, Composer, Year, playbackStatus

	
