# -*- encoding: utf-8 -*-
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

import Winamp
	
def run(MaxTandaLength):


	# Variable declaration
	
	Artist 		= []
	Album 		= []
	Title	 		= []
	Genre	 	= []
	Comment		= []
	Composer		= []
	Year			= []

		
	# Create a communications object
	winamp = Winamp.Winamp()
	
	
	if winamp.getPlaybackStatus() == 1:
	#	print "Lets get some info!"
		playbackStatus = 'Playing'

		#Declare our position
		currentsong	= winamp.getListPosition()
		listlength		= winamp.getListLength()

		# Extract previous song
		if currentsong == 0:
			searchsong = currentsong # Start on the current song
		else:
			searchsong = currentsong-1 # Start on previous song
		
		while searchsong < currentsong+MaxTandaLength+2 and searchsong < listlength:
			#try:
				TrackURL = winamp.getPlaylistFile(searchsong)
                #id3info = ID3(TrackURL)
				Artist.append(id3info.artist)
				Album.append(id3info.album)
				Title.append(id3info.title)
				Genre.append(str(id3info.genre)) # Comes as a number, need table to transfer
				Comment.append(id3info.comment)
				Year.append(id3info.year)
				
			#except:
				#break
				searchsong = searchsong+1
		return Artist, Album, Title, Genre, Comment, Composer, Year, playbackStatus
	
	else:
		playbackStatus = 'Stopped'
		return Artist, Album, Title, Genre, Comment, Composer, Year, playbackStatus
