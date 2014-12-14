
import sys

def pack( module, outdir, debug ):
	import zipfile, os

	assert os.path.exists( module )

	# pack
	zipname = os.path.join( outdir, module.replace( ' ', '_' ).replace( '-', '_' ) )
	if debug:
		zipname = zipname + '_Debug.oxt'
	else:
		zipname = zipname + '.oxt'
	def writesettings( filename ):
		settings = file( os.path.join( module, filename ), 'wb' )
		settings.write( 'DEBUG = %r\n'%debug )
		if debug:
			settings.write( 'HOME = %r\n'%os.path.join( os.getcwd(), module ) )		# debug mode extensions dynamically load code from the development source code
		settings.close()
	id = module.lower().replace( ' ', '' ).replace( '-', '' ).replace( '_', '' )
	writesettings( id + '_generatedsettings.py' )			# for the loader
	writesettings( os.path.join( id, 'generatedsettings.py' ) )	# for extensioncore
	z = zipfile.ZipFile( zipname, 'w', zipfile.ZIP_DEFLATED )
	for root, dirs, files in os.walk( module ):
		if '.svn' in dirs:
			dirs.remove( '.svn' )
		if 'DONTPACK' in dirs:
			dirs.remove( 'DONTPACK' )
		for f in files:
			f = os.path.join( root, f )
			sf = f[len( module ) + 1:]
			print 'Packing', f
			z.write( f, sf )
	z.close()
	print 'Created', zipname

LAUNCHPAD_URL = 'https://launchpad.net/eoec/'

def usage():
	print '''Pack EuroOffice Extension Creator project and create OXT file.
Run this command from the parent folder of the project. The OXT file will also be created here.

        pack.py [options] project-name

Options are:
    -h, --help                 this help
    -D, --debug                create debug version
    -d, --dir=DIR              create OXT file in DIR (defaults to current directory)
    
To learn more or get in touch, visit the Launchpad page of EuroOffice Extension Creator at
	%s
'''%LAUNCHPAD_URL


def main():
	import sys
	import getopt
	import os
	try:
		optlist, args = getopt.getopt( sys.argv[1:], 'hDd:', ['help', 'debug', 'dir='] )
	except getopt.GetoptError:
		usage()
		sys.exit( 2 )
	outpath = os.getcwd()
	debug = False
	for o, a in optlist:
		if o in ('-h', '--help'):
			usage()
			sys.exit()
		elif o in ('-D', '--debug'):
			debug = True
		elif o in ('-d', '--dir'):
			outpath = a
	if len( args ) != 1:
		usage()
		sys.exit( 2 )
	project = args[0]
	if project.endswith( '/' ):
		project = project[:-1]
	pack( project, outpath, debug )

if __name__ == '__main__':
	main()

