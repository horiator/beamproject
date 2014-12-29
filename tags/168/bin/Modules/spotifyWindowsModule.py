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
	import win32gui
except:
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

	# Check if Spotify is running and create a handle
	if ApplicationRunning("spotify.exe"):
		try:
			spotify = win32gui.FindWindow("SpotifyMainWindow", None)
		except:
			playbackStatus = 'Mediaplayer is not running'
			return Artist, Album, Title, Genre, Comment, Composer, Year, playbackStatus
	else:
		playbackStatus = 'Mediaplayer is not running'
		return Artist, Album, Title, Genre, Comment, Composer, Year, playbackStatus
	
	# Check if closed
	if win32gui.GetWindowText(spotify) == "":
		playbackStatus = 'Mediaplayer is not running'
		return Artist, Album, Title, Genre, Comment, Composer, Year, playbackStatus

	# Read from Spotify
	try:
		trackinfo = win32gui.GetWindowText(spotify).split(" - ")
		artist, title = trackinfo[1].split(" \x96 ")
		
		# Create empty previous
		Artist.append(artist)
		Title.append(title)
		Album.append("")
		Genre.append("")
		Comment.append("")
		Composer.append("")
		Year.append("")
		
		playbackStatus = 'Playing'
		return Artist, Album, Title, Genre, Comment, Composer, Year, playbackStatus
	
	except:
		playbackStatus = 'Paused'
		Artist.append("")
		Title.append("")
		Album.append("")
		Genre.append("")
		Comment.append("")
		Composer.append("")
		Year.append("")
		return Artist, Album, Title, Genre, Comment, Composer, Year, playbackStatus


def ApplicationRunning(AppName):
    import subprocess
    cmd = 'WMIC PROCESS get Caption,Commandline,Processid'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    for line in proc.stdout:
        if AppName in line:
            return True
    return False
