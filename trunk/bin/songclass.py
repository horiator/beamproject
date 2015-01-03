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

import platform, os, sys


class SongObject(object):

    def __init__(self, p_artist=None, p_album=None, p_title=None, p_genre=None
                 p_comment=None, p_composer=None, p_year=None, p_singer=None
                 p_albumArtist=None, p_performer = None, p_isCortina = None):
        self._artist      = p_artist
        self._album       = p_album
        self._title       = p_title
        self._genre       = p_genre
        self._comment     = p_comment
        self._composer    = p_composer
        self._year        = p_year
        self._singer      = p_singer
        self._albumArtist = p_albumArtist
        self._performer   = p_performer
        self._isCortina   = p_isCortina
        
    def __eq__(self, other)
        if isinstance(other, SongObject):
            return (self._artist == other._artist &&
                    self._album == other._album &&
                    self._title == other._title &&
                    self._genre == other._genre &&
                    self._comment = other._comment &&
                    self._composer == other._composer &&
                    self._year == other._year &&
                    self._albumArtist == other._albumArtist &&
                    self._performer == other._performer)
        else:
            return false
            
    
    def __ne__(self, other)
        if isinstance(other, SongObject):
            return (self._artist != other._artist ||
                    self._album != other._album ||
                    self._title != other._title ||
                    self._genre != other._genre ||
                    self._comment != other._comment ||
                    self._composer != other._composer ||
                    self._year != other._year ||
                    self._albumArtist != other._albumArtist ||
                    self._performer != other._performer)
        else:
            return false 
              
    def applyRules(self, rulesArray)
        for i in range(0, len(rulesArray)):
            currentRule = rulesArray[i]
            try:
                if currentRule[u'Type'] == 'Parse' and currentRule[u'Active'] == 'yes':
                    # Find Rule[u'Field2'] in Rule[u'Field1'],
                    # split Rule[u'Field1'] and save into Rule[u'Field3 and 4]
                    if str(Rule[u'Field2'].replace("%"," self.")) in str(eval(Rule[u'Field1'].replace("%"," self."))):
                        splitStrings = eval(str(Rule[u'Field1']).replace("%"," self."))[j].split(str(Rule[u'Field2']))
                        [eval(Rule[u'Field3'].replace("%"," self.")), eval(Rule[u'Field4'].replace("%"," self."))] = [splitStrings[0], splitStrings[1]]

                if Rule[u'Type'] == 'Cortina' and Rule[u'Active'] == 'yes':
                    # Rule[u'Field2'] == is: IsCortina[j] shall be 1 if Rule[u'Field1'] is Rule[u'Field3']
                    if Rule[u'Field2'] == 'is':
                        if eval(str(Rule[u'Field1']).replace("%"," self.")) in str(Rule[u'Field3']):
                            self.IsCortina[j] = 1
                    # Rule[u'Field2'] == is not: IsCortina[j] shall be 1 if Rule[u'Field1'] not in Rule[u'Field3']
                    if Rule[u'Field2'] == 'is not':
                        if eval(str(Rule[u'Field1']).replace("%"," self.")) not in str(Rule[u'Field3']):
                            self.IsCortina[j] = 1

                if Rule[u'Type'] == 'Copy' and Rule[u'Active'] == 'yes':
                    # Rule[u'Field1'] shall be Rule[u'Field2']
                    # Example:
                    # Singer(j) = Comment(j)
                    eval(str(Rule[u'Field2']).replace("%"," self.")) = eval(str(Rule[u'Field1']).replace("%"," self."))

                if Rule[u'Type'] == 'Mood' and Rule[u'Active'] == 'yes':
                    # Only apply Mood for current song (j==1)
                    if Rule[u'Field2'] == 'is':
                        if eval(str(Rule[u'Field1']).replace("%"," self.")) in str(Rule[u'Field3']) and str(Rule[u'PlayState']) in self.PlaybackStatus and j == 1:
                            self.CurrentMood = Rule[u'Name']
                            self.DisplaySettings = Rule[u'Display']
                            self.BackgroundImage = Rule[u'Background']
                    if Rule[u'Field2'] == 'is not':
                        if eval(str(Rule[u'Field1']).replace("%"," self.")) not in str(Rule[u'Field3']) and str(Rule[u'PlayState']) in self.PlaybackStatus and j == 1:
                            self.CurrentMood = Rule[u'Name']
                            self.DisplaySettings = Rule[u'Display']
                            self.BackgroundImage = Rule[u'Background']                              
                    # Only if playback is stopped and we have a mood for this
                    if self.PlaybackStatus == "Stopped":
                        if eval(str(Rule[u'Field1']).replace("%"," self.")) in str(Rule[u'Field2']) and str(Rule[u'PlayState']) in self.PlaybackStatus:
                            self.CurrentMood = Rule[u'Name']
                            self.DisplaySettings = Rule[u'Display']
                            self.BackgroundImage = Rule[u'Background']
            except:
                print "Error at Rule:", i,".Type:", Rule[u'Type'], ". First Field", Rule[u'Field1']
                break
    
    
