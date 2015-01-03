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

    def __init__(self, p_artist=u"", p_album=u"", p_title=u"", p_genre=u"",
                 p_comment=u"", p_composer=u"", p_year=u"", p_singer=u"",
                 p_albumArtist=u"", p_performer = u"", p_isCortina = 0):
        self.Artist      = p_artist
        self.Album       = p_album
        self.Title       = p_title
        self.Genre       = p_genre
        self.Comment     = p_comment
        self.Composer    = p_composer
        self.Year        = p_year
        self.Singer      = p_singer
        self.AlbumArtist = p_albumArtist
        self.Performer   = p_performer
        self.IsCortina   = p_isCortina
        
    def __eq__(self, other):
        if isinstance(other, SongObject):
            return (self.Artist == other.Artist           and
                    self.Album == other.Album             and
                    self.Title == other.Title             and
                    self.Genre == other.Genre             and
                    self.Comment == other.Comment         and
                    self.Composer == other.Composer       and
                    self.Year == other.Year               and
                    self.AlbumArtist == other.AlbumArtist and
                    self.Performer == other.Performer)
        else:
            return false
            
    
    def __ne__(self, other):
        if isinstance(other, SongObject):
            return (self.Artist != other.Artist           or
                    self.Album != other.Album             or
                    self.Title != other.Title             or
                    self.Genre != other.Genre             or
                    self.Comment != other.Comment         or
                    self.Composer != other.Composer       or
                    self.Year != other.Year               or
                    self.AlbumArtist != other.AlbumArtist or
                    self.Performer != other.Performer)
        else:
            return false 
              
    def applySongRules(self, rulesArray):
        for i in range(0, len(rulesArray)):
            currentRule = rulesArray[i]
            try:
                if currentRule[u'Type'] == 'Parse' and currentRule[u'Active'] == 'yes':
                    # Find currentRule[u'Field2'] in currentRule[u'Field1'],
                    # split currentRule[u'Field1'] and save into Rule[u'Field3 and 4]
                    if str(currentRule[u'Field2'].replace("%"," self.")) in eval(str(currentRule[u'Field1'].replace("%"," self."))):
                        splitStrings = eval(str(currentRule[u'Field1']).replace("%"," self.")).split(str(currentRule[u'Field2']))

                        eval(str(currentRule[u'Field3']).replace("%"," self.")) = "1"
                        print eval(str(currentRule[u'Field3']).replace("%"," self."))

                        print str(currentRule[u'Field3']).replace("%"," self."), "=" , splitStrings[0]
                        print str(currentRule[u'Field4']).replace("%"," self."), "=" , splitStrings[1]

                if currentRule[u'Type'] == 'Cortina' and currentRule[u'Active'] == 'yes':
                    # Rule[u'Field2'] == is: IsCortina[j] shall be 1 if Rule[u'Field1'] is Rule[u'Field3']
                    if Rule[u'Field2'] == 'is':
                        if eval(str(currentRule[u'Field1']).replace("%"," self.")) in str(currentRule[u'Field3']):
                            self.IsCortina = 1
                    # Rule[u'Field2'] == is not: IsCortina[j] shall be 1 if Rule[u'Field1'] not in Rule[u'Field3']
                    if Rule[u'Field2'] == 'is not':
                        if eval(str(currentRule[u'Field1']).replace("%"," self.")) not in str(currentRule[u'Field3']):
                            self.IsCortina = 1

                if currentRule[u'Type'] == 'Copy' and currentRule[u'Active'] == 'yes':
                    # Rule[u'Field1'] shall be Rule[u'Field2']
                    # Example:
                    # Singer(j) = Comment(j)
                    print str(currentRule[u'Field2']).replace("%","self.")
                    #eval(str(currentRule[u'Field2']).replace("%","self.")) = eval(str(currentRule[u'Field1']).replace("%"," self."))

            except:
                print "Error at Rule:", i,".Type:", currentRule[u'Type'], ". First Field", currentRule[u'Field1']
                break
    
    
