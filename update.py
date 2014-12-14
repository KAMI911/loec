LOEC_URL = 'https://github.com/KAMI911/loec'

def main():
	import sys
	import getopt
	import argparse
	parser = argparse.ArgumentParser(description='Update an EuroOffice Extension Creator project. Works by comparing file modification dates and overwrites files in the project that are older than the corresponding template file. The central ``myextension.py'' file is never overwritten.', epilog='To learn more or get in touch, visit the Launchpad page of LibreOffice Extension Creator at ' + LOEC_URL)
	parser.add_argument('--quiet', '-q', action='store_true', help='do not ask permission for overwriting')
	parser.add_argument('project', type=str, metavar='project-name', help='project name')
	args = parser.parse_args()
	quiet = args.quiet
	project = args.project
	import os
	cwd = os.getcwd()
	outdir = os.path.join( cwd, project )
	if not os.path.exists( outdir ):
		print ('%s does not exist!' % outdir)
		sys.exit( 2 )
	home = os.path.split( sys.argv[0] )[0]
	template = os.path.join( home, 'template' )
	
	# load vendor, prefix and url
	execfile( os.path.join( outdir, 'eoec.config' ), globals(), globals() )
	import LOECUtil
	replicator = LOECUtil.LOECUtil(project, vendor, prefix, url, LOEC_URL)
	def update( dry ):
		for root, dirs, files in os.walk( template ):
			for d in dirs:
				d_out = os.path.join( replicator.substitute( root ).replace( template, outdir ), replicator.substitute( d ) )
				if not os.path.exists( d_out ):
					if dry:
						print ('directory will be created: %s' % d_out)
					else:
						print ('Creating directory %s' % d_out)
						os.mkdir( d_out )
			for f in files:
				if 'dontupdate' in globals() and f in dontupdate:
					continue
				f_in = os.path.join( root, f )
				f_out = os.path.join( replicator.substitute( root ).replace( template, outdir ), replicator.substitute( f ) )
				if not os.path.exists( f_out ):
					if dry:
						print ('file will be created: %s' % f_out)
					else:
						print ('creating file %s' % f_out)
						contents = file( f_in, 'rb' ).read()
						file( f_out, 'wb' ).write( replicator.substitute( contents ) )
				elif os.stat( f_in ).st_mtime > os.stat( f_out ).st_mtime:
					if f == '%extensionname%.py':
						print ('skipping file: %s' % f_out)
					else:
						if dry:
							print ('File will be overwritten: %s' % f_out)
						else:
							print ('Overwriting %s' % f_out)
							contents = file( f_in, 'rb' ).read()
							file( f_out, 'wb' ).write( replicator.substitute( contents ) )
	if not quiet:
		update( dry=True )
		if raw_input( 'apply update? [y/N] ' ).lower().startswith( 'y' ):
			update( dry=False )
	else:
		update( dry=False )

if __name__ == '__main__':
	main()

