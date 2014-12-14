LAUNCHPAD_URL = 'https://launchpad.net/eoec/'

def usage():
	print '''Create new EuroOffice Extension Creator project.

        create.py [options] project-name

Options are:
    -h, --help                 this help
        --vendor=VENDOR        vendor name (needed)
    -p, --prefix=PREFIX        prefix for service names (defaults to "org.openoffice")
    -u, --url=URL              extension website (defaults to "http://extensions.services.openoffice.org/")
    
To learn more or get in touch, visit the Launchpad page of EuroOffice Extension Creator at
	%s
'''%LAUNCHPAD_URL


def main():
	import sys
	import getopt
	try:
		optlist, args = getopt.getopt( sys.argv[1:], 'hp:u:', ['help', 'vendor=', 'prefix=', 'url='] )
	except getopt.GetoptError:
		usage()
		sys.exit( 2 )
	vendor = None
	prefix = 'org.openoffice'
	url = 'http://extensions.services.openoffice.org/'
	for o, a in optlist:
		if o in ('-h', '--help'):
			usage()
			sys.exit()
		elif o == '--vendor':
			vendor = a
		elif o in ('-p', '--prefix'):
			prefix = a
		elif o in ('-u', '--url'):
			url = a
	if len( args ) != 1:
		usage()
		sys.exit( 2 )
	if vendor is None:
		print 'Please set a vendor name using --vendor='
		sys.exit( 2 )
	project = args[0]
	import os
	cwd = os.getcwd()
	outdir = os.path.join( cwd, project )
	if os.path.exists( outdir ):
		print '%s already exists!'%outdir
		sys.exit( 2 )
	os.mkdir( outdir )
	home = os.path.split( sys.argv[0] )[0]
	template = os.path.join( home, 'template' )

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

	for root, dirs, files in os.walk( template ):
		for d in dirs:
			d_out = os.path.join( substitute( root ).replace( template, outdir ), substitute( d ) )
			os.mkdir( d_out )
		for f in files:
			f_in = os.path.join( root, f )
			f_out = os.path.join( substitute( root ).replace( template, outdir ), substitute( f ) )
			contents = file( f_in, 'rb' ).read()
			file( f_out, 'wb' ).write( substitute( contents ) )	

if __name__ == '__main__':
	main()

