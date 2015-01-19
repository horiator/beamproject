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

import subprocess
try:
    import win32com.client
except ImportError:
    pass
    
def run(MaxTandaLength):


    # Variable declaration
    
    Artist      = []
    Album       = []
    Title           = []
    Genre       = []
    Comment = []
    Composer    = []
    Year            = []

        
    # Check if iTunes is running and create a communications object
    if ApplicationRunning("iTunes.exe"):
        try:
            itunes = win32com.client.gencache.EnsureDispatch ("iTunes.Application")
        except:
            playbackStatus = 'Mediaplayer is not running'
            return Artist, Album, Title, Genre, Comment, Composer, Year, playbackStatus
    else:
        playbackStatus = 'Mediaplayer is not running'
        return Artist, Album, Title, Genre, Comment, Composer, Year, playbackStatus
    
    
    if itunes.PlayerState == 1:
    #   print "Lets get some info!"
        playbackStatus = 'Playing'

        #Declare our position
        currentsong = itunes.CurrentTrack.PlayOrderIndex
        searchsong = currentsong # Start on the current song
        
        while searchsong < currentsong+MaxTandaLength+2:
            try:
                Track = itunes.CurrentTrack.Playlist.Tracks.Item(searchsong)
                Artist.append((Track.Artist).encode('latin-1'))
                Album.append((Track.Album).encode('latin-1'))
                Title.append((Track.Name).encode('latin-1'))
                Genre.append((Track.Genre).encode('latin-1'))
                Comment.append((Track.Comment).encode('latin-1'))
                Composer.append((Track.Composer).encode('latin-1'))
                Year.append(Track.Year)
                
            except:
                break
            searchsong = searchsong+1

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
            proc.kill()
            return True
    proc.kill()
    return False
