LOEC_URL = 'https://github.com/KAMI911/loec'

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
		SettingsFile = open( os.path.join( module, filename ), 'wb' )
		content = 'DEBUG = %s\n' % debug
		SettingsFile.write( content.encode('utf-8') )
		if debug:
			content = 'HOME = %s\n'%os.path.join( os.getcwd(), module )
			SettingsFile.write( content.encode('utf-8') )		# debug mode extensions dynamically load code from the development source code
		SettingsFile.close()
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
			print ('Packing %s' % f)
			z.write( f, sf )
	z.close()
	print ('Created %s.' % zipname)

def main():
	import sys
	import os
	import argparse
	parser = argparse.ArgumentParser(description='Pack LibreOffice Extension Creator project and create OXT file. Run this command from the parent folder of the project. The OXT file will also be created here.', epilog='To learn more or get in touch, visit the Launchpad page of LibreOffice Extension Creator at ' + LOEC_URL)
	parser.add_argument('--debug', '-D', action='store_true', help='create debug version')
	parser.add_argument('--dir', '-d', type=str, nargs=1, default=os.getcwd(), help='create OXT file in DIR (defaults to current directory)')
	parser.add_argument('project', type=str, metavar='project-name', help='project name')

	args = parser.parse_args()
	outpath = args.dir
	debug = args.debug
	project = args.project
	if project.endswith( '/' ):
		project = project[:-1]
	pack( project, outpath, debug )

if __name__ == '__main__':
	main()

