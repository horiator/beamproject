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
	Comment		= []
	Composer		= []
	Year			= []
	playbackStatus  = ''
	
	try:
	    bus = dbus.SessionBus()
	    player = bus.get_object('org.mpris.clementine', '/Player')
	    tracklist = bus.get_object('org.mpris.clementine', '/TrackList')
	except:
	    playbackStatus  = 'Media player not running'
	    return Artist, Album, Title, Genre, Comment, Composer, Year, playbackStatus
	
	# Playstatus: 0 = Playing, 1 = Paused, 2 = Stopped
	Status = player.GetStatus()[0] 
	
	if Status == 0:
		playbackStatus = 'Playing'
		
		#Declare our position
		currentsong	= tracklist.GetCurrentTrack()
		listlength		= tracklist.GetLength()

		# Extract previous song
		if currentsong == '0':
			searchsong = currentsong # Start on the current song
		else:
			searchsong = currentsong-1 # Start on previous song
			
		while searchsong < currentsong+MaxTandaLength+2 and listlength-1:
				Track = tracklist.GetMetadata(searchsong)
				try:
				    Artist.append((Track[u'artist']).encode('utf-8'))
				except:
				    Artist.append("")
				try:
				    Album.append((Track[u'album']).encode('utf-8'))
				except:
				     Album.append("")
				try:
				    Title.append((Track[u'title']).encode('utf-8'))
				except:
				     Title.append("")
				try:
				     Genre.append((Track[u'genre']).encode('utf-8'))
				except:
				    Genre.append("")
				try:
				    Comment.append((Track[u'comment']).encode('utf-8'))
				except:
				     Comment.append("")
				try:
				     Composer.append((Track[u'composer']).encode('utf-8'))
				except:
				     Composer.append("")
				try:			
				     Year.append(Track[u'year'])
				except:
				     Year.append("")
				searchsong = searchsong+1
					
		return Artist, Album, Title, Genre, Comment, Composer, Year, playbackStatus
	
	if Status == 1:
		playbackStatus = 'Paused'
		return Artist, Album, Title, Genre, Comment, Composer, Year, playbackStatus
		
	if Status == 2:
		playbackStatus = 'Stopped'
		return Artist, Album, Title, Genre, Comment, Composer, Year, playbackStatus