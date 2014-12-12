#!/usr/bin/env python
# -*- coding: utf-8 -*-
#    Copyright (C) 2014 Mikael Holber http://http://www.beam-project.com
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
#
#    Revision History:
#
#    XX/XX/2014 Version 1.0
#       - Initial release
#
# This Python file uses the following encoding: utf-8


def run(MaxTandaLength):

    import subprocess, sys

    # Variable declaration
    
    Artist      = []
    Album       = []
    Title           = []
    Genre       = []
    Comment     = []
    Composer        = []
    Year            = []

    try:
        check       = subprocess.check_output(["audtool", "--current-song"]).rstrip('\n')
    except:
        playbackStatus = 'Mediaplayer is not running'
        return Artist, Album, Title, Genre, Comment, Composer, Year, playbackStatus

    playbackStatus  = subprocess.check_output(["audtool", "--playback-status"]).rstrip('\n')
    
    # Break and return empty if nothing is playing
    if check in 'No song playing.': 
        playbackStatus = 'Stopped'
        return Artist, Album, Title, Genre, Comment, Composer, Year, playbackStatus
    elif playbackStatus in 'stopped': 
        playbackStatus = 'Stopped'
        return Artist, Album, Title, Genre, Comment, Composer, Year, playbackStatus
    elif playbackStatus in 'paused': 
        playbackStatus = 'Paused'
        return Artist, Album, Title, Genre, Comment, Composer, Year, playbackStatus
    elif playbackStatus in 'playing':
    #   print "Lets get some info!"
        playbackStatus = 'Playing'

    #Declare our position
    currentsong     = int(subprocess.check_output(["audtool", "--playlist-position"]).rstrip('\n'))
    playlistlength  = int(subprocess.check_output(["audtool", "--playlist-length"]).rstrip('\n'))

    # Extract previous song
    if currentsong == 1:
        searchsong = currentsong # Start on the current song
    else:
        searchsong = currentsong-1 # Start on previous song
        
    while searchsong < playlistlength+1 and searchsong < currentsong+MaxTandaLength+2:
        Artist.append(subprocess.check_output(  ["audtool", "--playlist-tuple-data", "artist",   str(searchsong)]).rstrip('\n'))
        Album.append(subprocess.check_output(   ["audtool", "--playlist-tuple-data", "album",    str(searchsong)]).rstrip('\n'))
        Title.append(subprocess.check_output(   ["audtool", "--playlist-tuple-data", "title",    str(searchsong)]).rstrip('\n'))
        Genre.append(subprocess.check_output(   ["audtool", "--playlist-tuple-data", "genre",    str(searchsong)]).rstrip('\n'))
        Comment.append(subprocess.check_output( ["audtool", "--playlist-tuple-data", "comment",  str(searchsong)]).rstrip('\n'))
        Composer.append(subprocess.check_output(["audtool", "--playlist-tuple-data", "composer", str(searchsong)]).rstrip('\n'))
        Year.append(subprocess.check_output(    ["audtool", "--playlist-tuple-data", "year",     str(searchsong)]).rstrip('\n'))
        searchsong = searchsong+1

    return Artist, Album, Title, Genre, Comment, Composer, Year, playbackStatus

