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
	Comment		= []
	Composer		= []
	Year			= []

		
	# Create a communications object
	if ApplicationRunning("MediaMonkey.exe"):
		try:
			MediaMonkey = win32com.client.Dispatch("SongsDB.SDBApplication")
		except:
			playbackStatus = 'Mediaplayer is not running'
			return Artist, Album, Title, Genre, Comment, Composer, Year, playbackStatus
	else:
			playbackStatus = 'Mediaplayer is not running'
			return Artist, Album, Title, Genre, Comment, Composer, Year, playbackStatus
	
	if MediaMonkey.Player.isPlaying and not MediaMonkey.Player.isPaused:
	#	print "Lets get some info!"
		playbackStatus = 'Playing'

		#Declare our position
		currentsong	= MediaMonkey.Player.CurrentSongIndex
		searchsong = currentsong # Start on the current song

		
		while searchsong < currentsong+MaxTandaLength+2:
			try:
				Track = MediaMonkey.Player.CurrentPlaylist.Item(searchsong)
				try:
				    Artist.append(Track.ArtistName.encode('latin-1'))
				except:
					Artist.append('')
				try:
					Album.append(Track.AlbumName.encode('latin-1'))
				except:
					Album.append('')
				try:
					Title.append(Track.Title.encode('latin-1'))
				except:
					Title.append('')
				try:
					Genre.append(Track.Genre.encode('latin-1'))
				except:
					Genre.append('')
				try:
					Comment.append(Track.Comment.encode('latin-1'))
				except:
					Comment.append('')
				try:
					Composer.append(Track.Author.encode('latin-1'))
				except:
					Composer.append('')
				try:
					Year.append(Track.Year)
				except:
					Year.append('')
			except:
				break
			searchsong = searchsong+1

		return Artist, Album, Title, Genre, Comment, Composer, Year, playbackStatus
	
	elif not MediaMonkey.Player.isPlaying:
		playbackStatus = 'Stopped'
		return Artist, Album, Title, Genre, Comment, Composer, Year, playbackStatus
		
	elif MediaMonkey.Player.isPaused and MediaMonkey.Player.isPlaying:
		playbackStatus = 'Paused'
		return Artist, Album, Title, Genre, Comment, Composer, Year, playbackStatus


def ApplicationRunning(AppName):
    import subprocess
    cmd = 'WMIC PROCESS get Caption,Commandline,Processid'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    for line in proc.stdout:
        if AppName in line:
            proc.kill()
            return True
    proc.kill()
    return False