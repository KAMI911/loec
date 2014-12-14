LAUNCHPAD_URL = 'https://launchpad.net/eoec/'

def usage():
	print '''Update an EuroOffice Extension Creator project.
Works by comparing file modification dates and overwrites files in the project that are
older than the corresponding template file. The central ``myextension.py'' file is
never overwritten.

        update.py [options] project-name

Options are:
    -h, --help                 this help
    -q, --quiet                do not ask permission for overwriting
    
To learn more or get in touch, visit the Launchpad page of EuroOffice Extension Creator at
	%s
'''%LAUNCHPAD_URL


def main():
	import sys
	import getopt
	try:
		optlist, args = getopt.getopt( sys.argv[1:], 'hq', ['help', 'quiet'] )
	except getopt.GetoptError:
		usage()
		sys.exit( 2 )
	quiet = False
	for o, a in optlist:
		if o in ('-h', '--help'):
			usage()
			sys.exit()
		elif o in ('-q', '--quiet'):
			quiet = True
	if len( args ) != 1:
		usage()
		sys.exit( 2 )
	project = args[0]
	import os
	cwd = os.getcwd()
	outdir = os.path.join( cwd, project )
	if not os.path.exists( outdir ):
		print '%s does not exist!'%outdir
		sys.exit( 2 )
	home = os.path.split( sys.argv[0] )[0]
	template = os.path.join( home, 'template' )
	
	# load vendor, prefix and url
	execfile( os.path.join( outdir, 'eoec.config' ), globals(), globals() )

	def substitute( text ):
		text = text.replace( '%Extension Name%', project )
		text = text.replace( '%Vendor Name%', vendor )
		for separator in ('', '-', '_'):
			id = project
			for sep in (' ', '-', '_', '.', ','):
				id = id.replace( sep, separator )
			text = text.replace( '%Extension' + separator + 'Name%', id )
			text = text.replace( '%extension' + separator + 'name%', id.lower() )
			id = vendor
			for sep in (' ', '-', '_', '.', ','):
				id = id.replace( sep, separator )
			text = text.replace( '%Vendor' + separator + 'Name%', id )
			text = text.replace( '%vendor' + separator + 'name%', id.lower() )
		text = text.replace( '%prefix%', prefix )
		text = text.replace( '%url%', url )
		text = text.replace( '%Creator Name%', 'EuroOffice Extension Creator (by MultiRacio Ltd.)' )
		text = text.replace( '%Creator Short Name%', 'EuroOffice Extension Creator' )
		text = text.replace( '%creator url%', LAUNCHPAD_URL )
		return text

	def update( dry ):
		for root, dirs, files in os.walk( template ):
			for d in dirs:
				d_out = os.path.join( substitute( root ).replace( template, outdir ), substitute( d ) )
				if not os.path.exists( d_out ):
					if dry:
						print 'directory will be created:', d_out
					else:
						print 'creating directory', d_out
						os.mkdir( d_out )
			for f in files:
				if 'dontupdate' in globals() and f in dontupdate:
					continue
				f_in = os.path.join( root, f )
				f_out = os.path.join( substitute( root ).replace( template, outdir ), substitute( f ) )
				if not os.path.exists( f_out ):
					if dry:
						print 'file will be created:', f_out
					else:
						print 'creating file', f_out
						contents = file( f_in, 'rb' ).read()
						file( f_out, 'wb' ).write( substitute( contents ) )
				elif os.stat( f_in ).st_mtime > os.stat( f_out ).st_mtime:
					if f == '%extensionname%.py':
						print 'skipping file:', f_out
					else:
						if dry:
							print 'file will be overwritten:', f_out
						else:
							print 'overwriting', f_out
							contents = file( f_in, 'rb' ).read()
							file( f_out, 'wb' ).write( substitute( contents ) )
	if not quiet:
		update( dry=True )
		if raw_input( 'apply update? [y/N] ' ).lower().startswith( 'y' ):
			update( dry=False )
	else:
		update( dry=False )

if __name__ == '__main__':
	main()

