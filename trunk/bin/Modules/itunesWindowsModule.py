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
	#try:
	itunes = win32com.client.gencache.EnsureDispatch ("iTunes.Application")
	#except:
	#	playbackStatus = 'Mediaplayer is not running'
	#	return Artist, Album, Title, Genre, Comment, Composer, Year, playbackStatus
	
	if itunes.PlayerState == 1:
	#	print "Lets get some info!"
		playbackStatus = 'Playing'

		#Declare our position
		currentsong	= itunes.CurrentTrack.PlayOrderIndex

		# Extract previous song
		if currentsong == 1:
			searchsong = currentsong # Start on the current song
		else:
			searchsong = currentsong-1 # Start on previous song
		
		while searchsong < currentsong+MaxTandaLength+2:
			try:
				Track = itunes.CurrentTrack.Playlist.Tracks.Item(searchsong)
				Artist.append(Track.Artist)
				Album.append(Track.Album)
				Title.append(Track.Name)
				Genre.append(Track.Genre)
				Comment.append(Track.Comment)
				Composer.append(Track.Composer)
				Year.append(Track.Year)
				searchsong = searchsong+1
			except:
				break
		return Artist, Album, Title, Genre, Comment, Composer, Year, playbackStatus
	
	else:
		playbackStatus = 'Stopped'
		return Artist, Album, Title, Genre, Comment, Composer, Year, playbackStatus
