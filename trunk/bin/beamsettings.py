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

import json, wx, platform
import io, os, sys


class BeamSettings:
    # Define Dictionaries
    # these are static class vriables
    FontTypeDictionary = {"Decorative":wx.DECORATIVE, # A decorative font
                    "Default":wx.FONTFAMILY_DEFAULT,
                    "Modern":wx.FONTFAMILY_MODERN,
                    "Roman":wx.FONTFAMILY_ROMAN,
                    "Script":wx.FONTFAMILY_SCRIPT,
                    "Swiss":wx.FONTFAMILY_SWISS,
                    "Teletype":wx.FONTFAMILY_TELETYPE
                    }
    FontWeightDictionary = {"Bold":wx.BOLD,
                   "Light":wx.FONTWEIGHT_LIGHT,
                   "Normal":wx.FONTWEIGHT_NORMAL
                    }
    FontStyleDictionary = {"Italic":wx.ITALIC,
                  "Normal":wx.FONTSTYLE_NORMAL,
                  "Slant":wx.FONTSTYLE_SLANT
                    }

    # strings resources JSON format
    filename = os.path.join(os.getcwd(), 'resources', 'text', 'strings.txt')
    stringResources = json.load(open(filename, "r"))

    defaultConfigFileName = stringResources["defaultConfigFileName"]
    mainFrameTitle = stringResources["mainFrameTitle"]
    aboutDialogDescription = stringResources["aboutDialogDescription"]
    aboutDialogLicense = stringResources["aboutDialogLicense"]
    aboutCopyright = stringResources["aboutCopyright"]
    aboutWebsite = stringResources["aboutWebsite"]
    aboutDeveloper = stringResources["aboutDeveloper"]
    aboutArtist = stringResources["aboutArtist"]

    def __init__(self):
        self._moduleSelected    = ''
        self._maxTandaLength    = ''
        self._updateTimer       = ''
        self._BackgroundPath    = ''

        self._allModulesSettings    = ''
        self._myDisplaySettings     = ''
        self._displayWhenStopped    = ''
        self._rules                 = ''

    def LoadConfig(self, inputConfigFile):

        # Load Settings
        ConfigFile = open(os.path.join(os.getcwd(), inputConfigFile), 'r')
        ConfigData = json.load(ConfigFile)             # Loading settings from the specfied file
        ConfigFile.close()
        
        #ConfigData = json.load(io.open(inputConfigFile,"r", encoding='utf8').read().decode("utf-8"))
        #print data                
        

        self._moduleSelected        = ConfigData[u'Module']         # Player to read from
        self._maxTandaLength        = ConfigData[u'MaxTandaLength'] # Longest tandas, optimize for performance
        self._updateTimer           = ConfigData[u'Updtime']        # mSec between reading
        self._stoppedStateBackgroundPath   = ConfigData[u'StoppedStateBackgroundImage'] # Relative path to StoppedStateBackground, use 1920x1080 for best performance
        self._playingStateBackgroundPath   = ConfigData[u'PlayingStateBackgroundImage']# Relative path to PlahyingStateBackground, use 1920x1080 for best performance

        # Dictionaries
        self._allModulesSettings    = ConfigData[u'AllModules']
        self._myDisplaySettings     = ConfigData[u'Display']
        self._displayWhenStopped    = ConfigData[u'DisplayWhenStopped']
        self._rules                 = ConfigData[u'Rules']

        # Set modules for operating system
        if platform.system() == 'Linux':
            tmp = self._allModulesSettings[0]
        if platform.system() == 'Windows':
            tmp = self._allModulesSettings[1]
        if platform.system() == 'Darwin':
            tmp = self._allModulesSettings[2]

        self._currentModules = [s.encode('utf-8') for s in tmp[u'Modules']]


        if self._moduleSelected == '':
            self._moduleSelected = [s.encode('utf-8') for s in tmp[u'Modules']][0]
        return


    def SaveConfig(self, outputConfigFile):
        # Create empty entity
        output = {}

        output[u'Configname']       = "Default Configuration"
        output[u'Comment']          = "This configuration works with version 0.2 of Beam"
        output[u'Author']           = "Mikael Holber & Horia Uifaleanu - 2014"
        output[u'Module']           = self._moduleSelected
        output[u'MaxTandaLength']   = self._maxTandaLength
        output[u'Updtime']          = self._updateTimer
        output[u'StoppedStateBackgroundImage']    = self._stoppedStateBackgroundPath
        output[u'PlayingStateBackgroundImage']    = self._playingStateBackgroundPath

        # Dictionaries
        output[u'AllModules']           = self._allModulesSettings
        output[u'Display']              = self._myDisplaySettings
        output[u'DisplayWhenStopped']   = self._displayWhenStopped
        output[u'Rules']                = self._rules

        # Write config file
        ConfigFile = open(os.path.join(os.getcwd(), outputConfigFile), 'w')
        json.dump(output, ConfigFile, indent=2)
        ConfigFile.close()
        
        #output_utf8 = output.encode('UTF-8')
        #open("test_utf8.json, 'w').write(output_utf8)
        
        return

beamSettings = BeamSettings()   # Create the settings object
