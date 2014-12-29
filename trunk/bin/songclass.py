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
                 p_albumArtist=None, p_isCortina = None):
        self._artist      = p_artist
        self._album       = p_album
        self._title       = p_title
        self._genre       = p_genre
        self._comment     = p_comment
        self._composer    = p_composer
        self._year        = p_year
        self._singer      = p_singer
        self._albumArtist = p_albumArtist
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
                    self._albumArtist == other._albumArtist)
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
                    self._albumArtist != other._albumArtist)
        else:
            return false    
    
    
