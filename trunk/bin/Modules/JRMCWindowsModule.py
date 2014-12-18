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

import subprocess
try:
	import win32com.client
except ImportError:
	pass
	
def run(MaxTandaLength):


	# Variable declaration
	
	Artist 		= []
	Album 		= []
	Title	 		= []
	Genre	 	= []
	Comment	= []
	Composer	= []
	Year			= []

	# Check if iTunes is running and create a communications object
	if ApplicationRunning("Media Center 20.exe"):
		try:
			JRMC = win32com.client.Dispatch ("MediaJukebox Application")
		except:
			playbackStatus = 'Mediaplayer is not running'
			return Artist, Album, Title, Genre, Comment, Composer, Year, playbackStatus
	else:
		playbackStatus = 'Mediaplayer is not running'
		return Artist, Album, Title, Genre, Comment, Composer, Year, playbackStatus
	
	
	if JRMC.GetPlayback().State == 2:
	#	print "Lets get some info!"
		playbackStatus = 'Playing'

		#Declare our position
		CurrentPlaylist = JRMC.GetCurPlaylist()
		currentsong	= CurrentPlaylist.Position

		# Extract previous song
		if currentsong == 2:
			searchsong = currentsong # Start on the current song
		else:
			searchsong = currentsong-1 # Start on previous song
		
		while searchsong < currentsong+MaxTandaLength+2:
			try:
				Track = CurrentPlaylist.GetFile(searchsong)
				Artist.append((Track.Artist).encode('latin-1'))
				Album.append((Track.Album).encode('latin-1'))
				Title.append((Track.Name).encode('latin-1'))
				Genre.append((Track.Genre).encode('latin-1'))
				Comment.append((Track.Comment).encode('latin-1'))
				Composer.append("")
				Year.append(Track.Year)
				
			except:
				break
			searchsong = searchsong+1

		return Artist, Album, Title, Genre, Comment, Composer, Year, playbackStatus
	
	elif JRMC.GetPlayback().State == 1:
		playbackStatus = 'Paused'
		return Artist, Album, Title, Genre, Comment, Composer, Year, playbackStatus
	else:
		playbackStatus = 'Stopped'
		return Artist, Album, Title, Genre, Comment, Composer, Year, playbackStatus


def ApplicationRunning(AppName):
    import subprocess
    cmd = 'WMIC PROCESS get Caption,Commandline,Processid'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    for line in proc.stdout:
        if AppName in line:
            return True
    return False