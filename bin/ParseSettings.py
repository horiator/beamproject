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
#    22/10/2014 Version 1.0
#    	- Initial release
#
import json, wx, platform

def LoadConfig(self):
	
	# Define Dictionaries
	self.FontTypeDictionary = {"Decorative":wx.DECORATIVE, # A decorative font
                    "Default":wx.FONTFAMILY_DEFAULT,
                    "Modern":wx.FONTFAMILY_MODERN,     
                    "Roman":wx.FONTFAMILY_ROMAN,      
                    "Script":wx.FONTFAMILY_SCRIPT,    
                    "Swiss":wx.FONTFAMILY_SWISS,      
                    "Teletype":wx.FONTFAMILY_TELETYPE     
		    }
	self.FontWeightDictionary = {"Bold":wx.BOLD,
                   "Light":wx.FONTWEIGHT_LIGHT,
                   "Normal":wx.FONTWEIGHT_NORMAL
                   }
 
        self.FontStyleDictionary = {"Italic":wx.ITALIC,
                  "Normal":wx.FONTSTYLE_NORMAL,
                  "Slant":wx.FONTSTYLE_SLANT
		    }
		    
	# Load Settings
	ConfigData = json.load(self.confFile)				# Loading settings from file

	self.ModuleSelected		= ConfigData[u'Module']			# Player to read from
	self.MaxTandaLength	= ConfigData[u'MaxTandaLength']	# Longest tandas, optimize for performance
	self.updateTimer 		= ConfigData[u'Updtime']		# mSec between reading
	self.BackgroundPath  	= ConfigData[u'Bgimage']		# Relative path to background, use 1920x1080 for best performance
	
	# Dictionaries
	self.AllModulesSettings	= ConfigData[u'AllModules']
	self.MyDisplaySettings	= ConfigData[u'Display']
	self.DisplayWhenStopped	= ConfigData[u'DisplayWhenStopped']
	self.Rules				= ConfigData[u'Rules']
	
	# Set modules for operating system
	if platform.system() == 'Linux':
		tmp = self.AllModulesSettings[0]
		self.AllModules = [s.encode('utf-8') for s in tmp[u'Modules']]
		if self.ModuleSelected == '':
			self.ModuleSelected = self.AllModules[0]
	if platform.system() == 'Windows':
		tmp = self.AllModulesSettings[1]
		self.AllModules = [s.encode('utf-8') for s in tmp[u'Modules']]
		if self.ModuleSelected == '':
			self.ModuleSelected = self.AllModules[0]
	if platform.system() == 'Darwin':
		tmp = self.AllModulesSettings[2]
		self.AllModules = [s.encode('utf-8') for s in tmp[u'Modules']]
		if self.ModuleSelected == '':
			self.ModuleSelected = self.AllModules[0]

	return

def SaveConfig(self):
	# Create empty entity
	output = {}
	
	output[u'Configname'] 		= "Default Configuration"
	output[u'Comment'] 			= "This configuration works with version 0.1 of DJ Display"
	output[u'Author']			= "Mikael Holber - 2014"
	output[u'Module'] 			= self.ModuleSelected
	output[u'MaxTandaLength'] 	= self.MaxTandaLength
	output[u'Updtime'] 			= self.updateTimer
	output[u'Bgimage'] 			= self.BackgroundPath
	
	# Dictionaries
	output[u'AllModules'] 			= self.AllModulesSettings
	output[u'Display'] 				= self.MyDisplaySettings
	output[u'DisplayWhenStopped'] 	= self.DisplayWhenStopped
	output[u'Rules']				= self.Rules
	
	# Write config file
	json.dump(output, self.confFile, indent=2)
	return
	
