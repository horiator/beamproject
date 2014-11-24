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
    
def run(MaxTandaLength):

	Artist 		= []
	Album 		= []
	Title	 		= []
	Genre	 	= []
	Comment		= []
	Composer		= []
	Year			= []
	playbackStatus  = ''
	
	#try:
	bus = dbus.SessionBus()
	banshee = bus.get_object("org.bansheeproject.Banshee", "/org/bansheeproject/Banshee/PlayerEngine")
	BansheeState = banshee.GetCurrentState()
	if BansheeState == 'playing':
		playbackStatus = 'Playing'
	elif BansheeState == 'paused':
		playbackStatus = 'Paused'
		return Artist, Album, Title, Genre, Comment, Composer, Year, playbackStatus
	else:
		playbackStatus = 'Stopped'
		return Artist, Album, Title, Genre, Comment, Composer, Year, playbackStatus
	#except:
	   # playbackStatus  = 'Media player not running'
	    #return Artist, Album, Title, Genre, Comment, Composer, Year, playbackStatus
	    
	# If I cannot find previous, then set them to nothing
	Artist.append('')
	Album.append('')
	Title.append('')
	Genre.append('')
	Comment.append('')
	Composer.append('')
	Year.append('')
	# Retrieve current song
	if playbackStatus == 'Playing':
		currentTrack = banshee.GetCurrentTrack()
		try:
			Artist.append(currentTrack[u'artist'].encode('utf-8'))
		except:
			Artist.append('')
		try:
			Title.append(currentTrack[u'name'].encode('utf-8'))
		except:
			Title.append('')
		try:
			Album.append(currentTrack[u'album'].encode('utf-8'))
		except:
			Album.append('')
		try:
			Genre.append(currentTrack[u'genre'].encode('utf-8'))
		except:
			Genre.append('')
		try:
			Comment.append(currentTrack[u'comment'].encode('utf-8'))
		except:
			Comment.append('')
		try:
			Composer.append(currentTrack[u'composer'].encode('utf-8'))
		except:
			Composer.append('')
		try:
			Year.append(currentTrack[u'year'])
		except:
			year.append('')
				
	return Artist, Album, Title, Genre, Comment, Composer, Year, playbackStatus
