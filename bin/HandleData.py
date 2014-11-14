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
#    	- Initial release
#
import subprocess, sys, wx
from Modules import audaciousModule, rhythmboxModule

def Init(self):

	# Initialize based on module selected

	if self.ModuleSelected in ('Audacious', 'Rhythmbox'):
		# If the configuration have a timer on how often to update the data
		try:
			# There is not timer, so create and start it
        		self.timer = wx.Timer(self)
        		self.Bind(wx.EVT_TIMER, self.updateData, self.timer)
			self.timer.Start(self.updateTimer)
		except:
			# There is already a timer restart with new update timing
			self.timer.Stop()
			self.timer.Start(self.updateTimer)

	if self.ModuleSelected in ('Traktor'):
		pass

	return 


########################################################################

def GetData(self):
	
	# Create local variables
	Artist 	= []
	Album 	= []
	Title 		= []
	Genre	= []
	Comment	= []
	Composer	= []
	Year		= []

	# Extract data using the player module
	if self.ModuleSelected == 'Audacious':
		Artist, Album, Title, Genre, Comment, Composer, Year, self.playbackStatus = audaciousModule.run(self.MaxTandaLength)
	if self.ModuleSelected == 'Rhythmbox':
		Artist, Album, Title, Genre, Comment, Composer, Year, self.playbackStatus = rhythmboxModule.run(self.MaxTandaLength)

	# Parse data using FilterData
	FilterData(self, Artist, Album, Title, Genre, Comment, Composer, Year, self.playbackStatus)
	
	return

#########################################################################
#
# Filterdata -
#	Filters the data from config file and displays it in DisplayRow
#	Rules are
#		RuleType:   Parse, NextTanda, Set
#		
#		 

def FilterData(self, Artist, Album, Title, Genre, Comment, Composer, Year, playbackStatus):

	Singer 	= [ "" for i in range(len(Artist)) ] # Does not exist in ID3
	IsCortina 	= [ 0 for i in range(len(Artist)) ] # Sets 1 if song is cortina

	#
	# Apply rules, for every song in list
	# 	
	for j in range(0, len(Artist)):
		for i in range(0, len(self.Rules)):
			Rule = self.Rules[i]
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
		for j in range(0, len(self.MyDisplaySettings)):
			MyDisplay = self.MyDisplaySettings[j]
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
				except:
					self.DisplayRow[j] = ''
				

	return 

	
