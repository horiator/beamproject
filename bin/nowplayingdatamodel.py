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

import wx, platform, os, sys
import time
from bin.beamsettings import *

if platform.system() == 'Linux':
    from Modules import audaciousModule, rhythmboxModule, clementineModule, bansheeModule
if platform.system() == 'Windows':
    from Modules import itunesWindowsModule, winampWindowsModule, MediaMonkeyModule, JRMCWindowsModule, spotifyWindowsModule

class NowPlayingDataModel:

    def __init__(self):
        
        songNo = eval(beamSettings._maxTandaLength + "+2")
        
        self.Artist      = [None] * songNo
        self.Album       = [None] * songNo
        self.Title       = [None] * songNo
        self.Genre       = [None] * songNo
        self.Comment     = [None] * songNo
        self.Composer    = [None] * songNo
        self.Year        = [None] * songNo
        self.Singer      = [None] * songNo
        self.IsCortina   = [None] * songNo

        self.PlaybackStatus = ""
        self.PreviousPlaybackStatus = ""
        self.PreviouslyPlayedSong = [ '' for i in range(7) ]
        
        self.NextTanda = [ '' for i in range(7) ]

        self.DisplayRow = []
        


        self.convDict = dict()
        
    def ExtractPlaylistInfo(self):
        
        self.PreviousPlaybackStatus = self.PlaybackStatus
        
        # Extract data using the player module
        if beamSettings._moduleSelected == 'Audacious':
            self.Artist, self.Album, self.Title, self.Genre, self.Comment, self.Composer, self.Year, self.PlaybackStatus = audaciousModule.run(beamSettings._maxTandaLength)
        if beamSettings._moduleSelected == 'Rhythmbox':
            self.Artist, self.Album, self.Title, self.Genre, self.Comment, self.Composer, self.Year, self.PlaybackStatus = rhythmboxModule.run(beamSettings._maxTandaLength)
        if beamSettings._moduleSelected == 'Itunes':
            self.Artist, self.Album, self.Title, self.Genre, self.Comment, self.Composer, self.Year, self.PlaybackStatus = itunesWindowsModule.run(beamSettings._maxTandaLength)
        if beamSettings._moduleSelected == 'Clementine':
            self.Artist, self.Album, self.Title, self.Genre, self.Comment, self.Composer, self.Year, self.PlaybackStatus = clementineModule.run(beamSettings._maxTandaLength)
        if beamSettings._moduleSelected == 'Banshee':
            self.Artist, self.Album, self.Title, self.Genre, self.Comment, self.Composer, self.Year, self.PlaybackStatus = bansheeModule.run(beamSettings._maxTandaLength)
        try: #required due to loaded modules
            if beamSettings._moduleSelected == 'Winamp':
                self.Artist, self.Album, self.Title, self.Genre, self.Comment, self.Composer, self.Year, self.PlaybackStatus = winampWindowsModule.run(beamSettings._maxTandaLength)
        except:
            pass
        if beamSettings._moduleSelected == 'MediaMonkey':
            self.Artist, self.Album, self.Title, self.Genre, self.Comment, self.Composer, self.Year, self.PlaybackStatus = MediaMonkeyModule.run(beamSettings._maxTandaLength)
        if beamSettings._moduleSelected == 'JRiver Media Center':
            self.Artist, self.Album, self.Title, self.Genre, self.Comment, self.Composer, self.Year, self.PlaybackStatus =JRMCWindowsModule.run(beamSettings._maxTandaLength)
        if beamSettings._moduleSelected == 'Spotify':
            self.Artist, self.Album, self.Title, self.Genre, self.Comment, self.Composer, self.Year, self.PlaybackStatus =spotifyWindowsModule.run(beamSettings._maxTandaLength)
          
        #if it's first update
        if self.PreviousPlaybackStatus == "":
            self.PreviousPlaybackStatus = self.PlaybackStatus
    #Process and Filter the freshly extracted Data
        
        self.Singer  = [ "" for i in range(len(self.Artist)) ] # Does not exist in ID3
        self.IsCortina   = [ 0 for i in range(len(self.Artist)) ] # Sets 1 if song is cortina

      
        #
        # Apply rules, for every song in list
        #
        for j in range(0, len(self.Artist)):
            for i in range(0, len(beamSettings._rules)):
                Rule = beamSettings._rules[i]
                try:
                    if Rule[u'Type'] == 'Parse' and Rule[u'Active'] == 'yes':
                        # Find Rule[u'Field2'] in Rule[u'Field1'],
                        # split Rule[u'Field1'] and save into Rule[u'Field3 and 4]
                        if str(Rule[u'Field2'].replace("%"," self.")) in str(eval(Rule[u'Field1'].replace("%"," self."))[j]):
                            splitStrings = eval(str(Rule[u'Field1']).replace("%"," self."))[j].split(str(Rule[u'Field2']))
                            [eval(Rule[u'Field3'].replace("%"," self."))[j], eval(Rule[u'Field4'].replace("%"," self."))[j]] = [splitStrings[0], splitStrings[1]]

                    if Rule[u'Type'] == 'Cortina' and Rule[u'Active'] == 'yes':
                        # Rule[u'Field2'] == is: IsCortina[j] shall be 1 if Rule[u'Field1'] is Rule[u'Field3']
                        if Rule[u'Field2'] == 'is':
                            if eval(str(Rule[u'Field1']).replace("%"," self."))[j] in str(Rule[u'Field3']):
                                self.IsCortina[j] = 1
                        # Rule[u'Field2'] == is not: IsCortina[j] shall be 1 if Rule[u'Field1'] not in Rule[u'Field3']
                        if Rule[u'Field2'] == 'is not':
                            if eval(str(Rule[u'Field1']).replace("%"," self."))[j] not in str(Rule[u'Field3']):
                                self.IsCortina[j] = 1

                    if Rule[u'Type'] == 'Set' and Rule[u'Active'] == 'yes':
                        # Rule[u'Field1'] shall be Rule[u'Field2']
                        # Example:
                        # Singer(j) = Comment(j)
                        eval(str(Rule[u'Field2']).replace("%"," self."))[j] = eval(str(Rule[u'Field1']).replace("%"," self."))[j]
                except:
                    print "Error at Rule:", i,".Type:", Rule[u'Type'], ". First Field", Rule[u'Field1']
                    break
                    
        #
        # Create NextTanda
        #                    
        
        if self.PreviousPlaybackStatus in 'Playing':
            try:
                self.PreviouslyPlayedSong = [self.Artist[0], self.Album[0], self.Title[0], self.Genre[0], self.Comment[0], self.Composer[0], self.Year[0]]
            except:
                pass

        #
        # Create NextTanda
        #
        self.NextTanda = [ '' for i in range(7) ]
        for j in range(1, len(self.Artist)-1):
            # Check if song is cortina
            if self.IsCortina[j] and not self.IsCortina[j+1]:
                self.NextTanda = [self.Artist[j+1], self.Album[j+1], self.Title[j+1], self.Genre[j+1], self.Comment [j+1], self.Composer[j+1], self.Year[j+1]]
                break
        #
        # Create Display Strings
        #
        
        # The display lines
        for i in range(0, len(beamSettings._myDisplaySettings)): self.DisplayRow.append('')
        
        #first, update the conversion dictionary
        self.updateConversionDisctionary()
        
        if self.PlaybackStatus in 'Playing':
            for j in range(0, len(beamSettings._myDisplaySettings)):
                MyDisplay = beamSettings._myDisplaySettings[j]
                try:
                    displayValue = str(MyDisplay['Field'])
                except:
                    displayValue = unicode(MyDisplay['Field'])
                for key in self.convDict:
                    try:
                        displayValue = displayValue.replace(str(key), str(self.convDict[key]))
                    except:
                       displayValue = displayValue.replace(key.decode('utf-8'), self.convDict[key].decode('utf-8'))
                     
                if MyDisplay['HideControl']  == "":
                    self.DisplayRow[j] = displayValue
                else:
                    # Hides line if HideControl is empty if there is no next tanda
                    hideControlEval = str(MyDisplay['HideControl'])
                    for key in self.convDict:
                        hideControlEval = hideControlEval.replace(str(key), str(self.convDict[key]))
                        
                    if  not hideControlEval == "":
                        self.DisplayRow[j] = displayValue
                    else:
                        self.DisplayRow[j] = ""
        print "data updated: ", time.strftime("%H:%M:%S")
        return
    
    def updateConversionDisctionary(self):
        self.convDict = dict()
        #CurrentSong
        try:
            self.convDict['%Artist']    = self.Artist[1]
            self.convDict['%Album']     = self.Album[1]
            self.convDict['%Title']     = self.Title[1]
            self.convDict['%Genre']     = self.Genre[1]
            self.convDict['%Comment']   = self.Genre[1]
            self.convDict['%Composer']  = self.Composer[1]
            self.convDict['%Year']      = self.Year[1]
            self.convDict['%Singer']    = self.Singer[1]
            self.convDict['%IsCortina'] = self.IsCortina[1]
        except:
            self.convDict['%Artist']    = u""
            self.convDict['%Album']     = u""
            self.convDict['%Title']     = u""
            self.convDict['%Genre']     = u""
            self.convDict['%Comment']   = u""
            self.convDict['%Composer']  = u""
            self.convDict['%Year']      = u""
            self.convDict['%Singer']    = u""
            self.convDict['%IsCortina'] = u""
            
        #PreviousSong
        try:
            self.convDict['%PreviousArtist']    = self.PreviouslyPlayedSong[0]
            self.convDict['%PreviousAlbum']     = self.PreviouslyPlayedSong[1]
            self.convDict['%PreviousTitle']     = self.PreviouslyPlayedSong[2]
            self.convDict['%PreviousGenre']     = self.PreviouslyPlayedSong[3]
            self.convDict['%PreviousComment']   = self.PreviouslyPlayedSong[4]
            self.convDict['%PreviousComposer']  = self.PreviouslyPlayedSong[5]
            self.convDict['%PreviousYear']      = self.PreviouslyPlayedSong[6]
        except:
            self.convDict['%PreviousArtist']    = u""
            self.convDict['%PreviousAlbum']     = u""
            self.convDict['%PreviousTitle']     = u""
            self.convDict['%PreviousGenre']     = u""
            self.convDict['%PreviousComment']   = u""
            self.convDict['%PreviousComposer']  = u""
            self.convDict['%PreviousYear']      = u""
            
        #NextSong
        try:
            self.convDict['%NextArtist']    = self.Artist[1]
            self.convDict['%NextAlbum']     = self.Album[1]
            self.convDict['%NextTitle']     = self.Title[1]
            self.convDict['%NextGenre']     = self.Genre[1]
            self.convDict['%NextComment']   = self.Genre[1]
            self.convDict['%NextComposer']  = self.Composer[1]
            self.convDict['%NextYear']      = self.Year[1]
            self.convDict['%NextSinger']    = self.Singer[1]
            self.convDict['%NextIsCortina'] = self.IsCortina[1]
        except:
            self.convDict['%NextArtist']    = u""
            self.convDict['%NextAlbum']     = u""
            self.convDict['%NextTitle']     = u""
            self.convDict['%NextGenre']     = u""
            self.convDict['%NextComment']   = u""
            self.convDict['%NextComposer']  = u""
            self.convDict['%NextYear']      = u""
            self.convDict['%NextSinger']    = u""
            self.convDict['%NextIsCortina'] = u""
        
        #NextTanda
        try:
            self.convDict['%NextTandaArtist']   = self.NextTanda[0]
            self.convDict['%NextTandaAlbum']    = self.NextTanda[1]
            self.convDict['%NextTandaTitle']    = self.NextTanda[2]
            self.convDict['%NextTandaGenre']    = self.NextTanda[3]
            self.convDict['%NextTandaComment']  = self.NextTanda[4]
            self.convDict['%NextTandaComposer'] = self.NextTanda[5]
            self.convDict['%NextTandaYear']     = self.NextTanda[6]
        except:
            self.convDict['%NextTandaArtist']   = u""
            self.convDict['%NextTandaAlbum']    = u""
            self.convDict['%NextTandaTitle']    = u""
            self.convDict['%NextTandaGenre']    = u""
            self.convDict['%NextTandaComment']  = u""
            self.convDict['%NextTandaComposer'] = u""
            self.convDict['%NextTandaYear']     = u""
            
            
        #date and time
        
        self.convDict['%Hour']      = time.strftime("%H")
        self.convDict['%Min']       = time.strftime("%M")
        try:
            self.convDict['%Day']       = time.strftime("%e") # Does not work on Windows
        except:
            self.convDict['%Day']       = time.strftime("%d")
        self.convDict['%Month']     = time.strftime("%m")
        self.convDict['%Year']      = time.strftime("%Y")
        self.convDict['%LongDate']  = time.strftime("%d %B %Y")

    
nowPlayingDataModel = NowPlayingDataModel()   # Create the data model object
