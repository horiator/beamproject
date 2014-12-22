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
	spotify_bus = bus.get_object("org.mpris.MediaPlayer2.spotify", "/org/mpris/MediaPlayer2")
	spotify = dbus.Interface(spotify_bus,"org.mpris.MediaPlayer2.Player")
	properties_manager = dbus.Interface(spotify_bus, 'org.freedesktop.DBus.Properties')
	metadata = properties_manager.Get('org.mpris.MediaPlayer2.Player', 'Metadata')
	playbackStatus = properties_manager.Get('org.mpris.MediaPlayer2.Player', 'PlaybackStatus')

	#except:
	#	playbackStatus  = 'Media player not running'
	#	return Artist, Album, Title, Genre, Comment, Composer, Year, playbackStatus
		
	if playbackStatus == 'Paused':
		print "Paused"
		return Artist, Album, Title, Genre, Comment, Composer, Year, playbackStatus

	# Retrieve current song
	if playbackStatus == 'Playing':

		try:
			Artist.append(metadata['xesam:artist'][0].encode('utf-8'))
		except:
			Artist.append('')
		try:
			Title.append(metadata['xesam:title'].encode('utf-8'))
		except:
			Title.append('')
		try:
			Album.append(metadata['xesam:album'].encode('utf-8'))
		except:
			Album.append('')
		Genre.append('')
		Comment.append('')
		Composer.append('')
		try:
			Year.append(metadata['xesam:contentCreated'][:4])
		except:
			Year.append('')

	return Artist, Album, Title, Genre, Comment, Composer, Year, playbackStatus
