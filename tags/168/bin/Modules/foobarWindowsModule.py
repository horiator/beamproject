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
    if ApplicationRunning("foobar2000.exe"):
        try:
            Foobar = win32com.client.Dispatch("Foobar2000.Application.0.7")
        except:
            playbackStatus = 'Mediaplayer is not running'
            return Artist, Album, Title, Genre, Comment, Composer, Year, playbackStatus
    else:
        playbackStatus = 'Mediaplayer is not running'
        return Artist, Album, Title, Genre, Comment, Composer, Year, playbackStatus
    
    
    if Foobar.Playback.IsPlaying and not Foobar.Playback.IsPaused:
    #   print "Lets get some info!"
        playbackStatus = 'Playing'
        try:
            Artist.append(Foobar.Playback.FormatTitle("[%artist%]").encode('latin-1'))
        except:
            Artist.append('')
        try:
            Album.append(Foobar.Playback.FormatTitle("[%album%]").encode('latin-1'))
        except:
            Album.append('')
        try:
            Title.append(Foobar.Playback.FormatTitle("[%title%]").encode('latin-1'))
        except:
            Title.append('')
        try:
            Genre.append(Foobar.Playback.FormatTitle("[%genre%]").encode('latin-1'))
        except:
            Genre.append('')
        try:
            Comment.append(Foobar.Playback.FormatTitle("[%comment%]").encode('latin-1'))
        except:
            Comment.append('')
        try:
            Composer.append(Foobar.Playback.FormatTitle("[%composer%]").encode('latin-1'))
        except:
            Composer.append('')
        try:
            Year.append(Foobar.Playback.FormatTitle("[%date%]"))
        except:
            Year.append('')

        return Artist, Album, Title, Genre, Comment, Composer, Year, playbackStatus
    
    elif not Foobar.Playback.IsPlaying:
        playbackStatus = 'Stopped'
        return Artist, Album, Title, Genre, Comment, Composer, Year, playbackStatus

    elif Foobar.Playback.IsPlaying and Foobar.Playback.IsPaused:
        playbackStatus = 'Paused'
        return Artist, Album, Title, Genre, Comment, Composer, Year, playbackStatus

def ApplicationRunning(AppName):
    import subprocess
    cmd = 'WMIC PROCESS get Caption,Commandline,Processid'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    for line in proc.stdout:
        if AppName in line:
            return True
    return False
