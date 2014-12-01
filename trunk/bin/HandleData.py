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
#
#    Revision History:
#
#    XX/XX/2014 Version 1.0
#       - Initial release
#

import subprocess, sys, wx, platform
from bin.beamsettings import *

if platform.system() == 'Linux':
    from Modules import audaciousModule, rhythmboxModule, clementineModule, bansheeModule
if platform.system() == 'Windows':
    from Modules import itunesWindowsModule, winampWindowsModule, MediaMonkeyModule

########################################################################

def GetData(self):

    # Create local variables
    Artist  = []
    Album   = []
    Title       = []
    Genre   = []
    Comment = []
    Composer    = []
    Year        = []

    # Extract data using the player module
    if beamSettings._moduleSelected == 'Audacious':
        Artist, Album, Title, Genre, Comment, Composer, Year, self.playbackStatus = audaciousModule.run(beamSettings._maxTandaLength)
    if beamSettings._moduleSelected == 'Rhythmbox':
        Artist, Album, Title, Genre, Comment, Composer, Year, self.playbackStatus = rhythmboxModule.run(beamSettings._maxTandaLength)
    if beamSettings._moduleSelected == 'Itunes':
        Artist, Album, Title, Genre, Comment, Composer, Year, self.playbackStatus = itunesWindowsModule.run(beamSettings._maxTandaLength)
    if beamSettings._moduleSelected == 'Clementine':
        Artist, Album, Title, Genre, Comment, Composer, Year, self.playbackStatus = clementineModule.run(beamSettings._maxTandaLength)
    if beamSettings._moduleSelected == 'Banshee':
        Artist, Album, Title, Genre, Comment, Composer, Year, self.playbackStatus = bansheeModule.run(beamSettings._maxTandaLength)
    try: #required due to loaded modules
        if beamSettings._moduleSelected == 'Winamp':
            Artist, Album, Title, Genre, Comment, Composer, Year, self.playbackStatus = winampWindowsModule.run(beamSettings._maxTandaLength)
    except:
        pass
    if beamSettings._moduleSelected == 'MediaMonkey':
        Artist, Album, Title, Genre, Comment, Composer, Year, self.playbackStatus = MediaMonkeyModule.run(beamSettings._maxTandaLength)

    # Parse data using FilterData
    FilterData(self, Artist, Album, Title, Genre, Comment, Composer, Year, self.playbackStatus)

    return


#########################################################################
#
# Filterdata -
#   Filters the data from config file and displays it in DisplayRow
#   Rules are
#       RuleType:   Parse, NextTanda, Set
#
#

def FilterData(self, Artist, Album, Title, Genre, Comment, Composer, Year, playbackStatus):

    Singer  = [ "" for i in range(len(Artist)) ] # Does not exist in ID3
    IsCortina   = [ 0 for i in range(len(Artist)) ] # Sets 1 if song is cortina

    #
    # Apply rules, for every song in list
    #
    for j in range(0, len(Artist)):
        for i in range(0, len(beamSettings._rules)):
            Rule = beamSettings._rules[i]
            if Rule[u'Type'] == 'Parse' and Rule[u'Active'] == 'yes':
                # Find Rule[u'Field2'] in Rule[u'Field1'],
                # split Rule[u'Field1'] and save into Rule[u'Field3 and 4]
                if str(Rule[u'Field2']) in str(eval(Rule[u'Field1'])[j]):
                    splitStrings = eval(str(Rule[u'Field1']))[j].split(str(Rule[u'Field2']))
                    [eval(Rule[u'Field3'])[j], eval(Rule[u'Field4'])[j]] = [splitStrings[0], splitStrings[1]]

            if Rule[u'Type'] == 'Cortina' and Rule[u'Active'] == 'yes':
                # Rule[u'Field2'] == is: IsCortina[j] shall be 1 if Rule[u'Field1'] is Rule[u'Field3']
                if Rule[u'Field2'] == 'is':
                    if str(eval(Rule[u'Field1'])[j]) in str(Rule[u'Field3']):
                        IsCortina[j] = 1
                # Rule[u'Field2'] == is not: IsCortina[j] shall be 1 if Rule[u'Field1'] not in Rule[u'Field3']
                if Rule[u'Field2'] == 'is not':
                    if str(eval(Rule[u'Field1'])[j]) not in str(Rule[u'Field3']):
                        IsCortina[j] = 1

            if Rule[u'Type'] == 'Set' and Rule[u'Active'] == 'yes':
                # Rule[u'Field1'] shall be Rule[u'Field2']
                # Example:
                # Singer(j) = Comment(j)
                eval(str(Rule[u'Field2']))[j] = eval(str(Rule[u'Field1']))[j]
    #
    # Create NextTanda
    #
    NextTanda = [ [] for i in range(7) ]
    for j in range(1, len(Artist)-1):
        # Check if song is cortina
        if IsCortina[j] and not IsCortina[j+1]:
            NextTanda = [Artist[j+1], Album[j+1], Title[j+1], Genre[j+1], Comment [j+1], Composer[j+1], Year[j+1]]
        if IsCortina[j] and IsCortina[j+1]:
            break
    #
    # Display
    #
    if self.playbackStatus in 'Playing':
        for j in range(0, len(beamSettings._myDisplaySettings)):
            MyDisplay = beamSettings._myDisplaySettings[j]
            if MyDisplay['HideControl']  == "":
                try:
                    self.DisplayRow[j] = eval(MyDisplay['Field'])
                except:
                    pass
            else:
                # Hides line if HideControl is empty if there is no next tanda
                try:
                    if  not eval(MyDisplay['HideControl']) == []:
                        try:
                            self.DisplayRow[j] = eval(MyDisplay['Field'])
                        except:
                            self.DisplayRow[j] = MyDisplay['Field']
                    else:
                        self.DisplayRow[j] = ""
                except:
                    self.DisplayRow[j] = ""


    return


