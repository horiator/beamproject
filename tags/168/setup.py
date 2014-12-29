from distutils.core import setup
import py2exe

includes = []
excludes = ['_gtkagg', '_tkagg', 'bsddb', 'curses', 'email', 'pywin.debugger',
	'pywin.debugger.dbgcon', 'pywin.dialogs', 'tcl',
	'Tkconstants', 'Tkinter']

packages = []
dll_excludes = ['libgdk-win32-2.0-0.dll', 'libgobject-2.0-0.dll', 'tcl84.dll',
	'tk84.dll']
	
setup(windows=[{"script": "Beam.py",
	"icon_resources": [(1, "resources\icons\installer_icon\icon_Microsoft_48px.ico")]}], 
	options = {"py2exe": {"compressed": 2, 
	"optimize": 2,
	"includes": includes,
	"excludes": excludes,
	"packages": packages,
	"dll_excludes": dll_excludes,
	"bundle_files": 3,
	"dist_dir": "dist",
	"xref": False,
	"skip_archive": False,
	"ascii": False,
	"typelibs": [('{9E93C96F-CF0D-43F6-8BA8-B807A3370712}',0,1,13)]}},
	)
	