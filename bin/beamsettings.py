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

import json, wx, platform, os


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
    stringResources = json.load(open(os.getcwd() + "/resources/text/strings.txt", "r"))

    defaultConfigFileName = stringResources["defaultConfigFileName"]
    mainFrameTitle = stringResources["mainFrameTitle"]
    
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
        ConfigData = json.load(inputConfigFile)             # Loading settings from the specfied file

        self._moduleSelected        = ConfigData[u'Module']         # Player to read from
        self._maxTandaLength        = ConfigData[u'MaxTandaLength'] # Longest tandas, optimize for performance
        self._updateTimer           = ConfigData[u'Updtime']        # mSec between reading
        self._backgroundPath        = ConfigData[u'Bgimage']        # Relative path to background, use 1920x1080 for best performance
        
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
        output[u'Comment']          = "This configuration works with version 0.1 of DJ Display"
        output[u'Author']           = "Mikael Holber - 2014"
        output[u'Module']           = self._moduleSelected
        output[u'MaxTandaLength']   = self._maxTandaLength
        output[u'Updtime']          = self._updateTimer
        output[u'Bgimage']          = self._backgroundPath
        
        # Dictionaries
        output[u'AllModules']           = self._allModulesSettings
        output[u'Display']              = self._myDisplaySettings
        output[u'DisplayWhenStopped']   = self._displayWhenStopped
        output[u'Rules']                = self._rules
        
        # Write config file
        json.dump(output, outputConfigFile, indent=2)
        return

beamSettings = BeamSettings()   # Create the settings object
