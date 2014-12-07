from distutils.core import setup
import py2exe
 
setup(windows=['Beam.py'], options = {'py2exe':{'bundle_files':1}},ipfile = None,)
	