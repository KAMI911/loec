LOEC_URL = 'https://github.com/KAMI911/loec'

def main():
	import argparse
	import sys
	parser = argparse.ArgumentParser(description='Create new LibreOffice Extension Creator project.', epilog='To learn more or get in touch, visit the Launchpad page of LibreOffice Extension Creator at ' + LOEC_URL)
	parser.add_argument('--vendor', '-v', type=str, nargs=1, required=True, help='vendor name')
	parser.add_argument('--prefix', '-p', type=str, nargs=1, default='org.libreoffice', required=False, help='prefix for service names')
	parser.add_argument('--url', '-u', type=str, nargs=1, default='http://extensions.libreoffice.org/', required=False, help='extension website')
	parser.add_argument('project', type=str, metavar='project-name', help='project name')

	args = parser.parse_args()
	vendor = args.vendor[0]
	prefix = args.prefix
	url = args.url
	project = args.project
	DirCounter=0
	FileCounter=0
	import os
	cwd = os.getcwd()
	outdir = os.path.join( cwd, project )
	if os.path.exists( outdir ):
		print ('%s already exists!' % outdir)
		sys.exit( 2 )
	os.mkdir( outdir )
	home, file = os.path.split(os.path.realpath(__file__))
	template = os.path.join( home, 'template' )
	import LOECUtil
	replicator = LOECUtil.LOECUtil(project, vendor, prefix, url, LOEC_URL)
	for root, dirs, files in os.walk( template ):
		for d in dirs:
			d_out = os.path.join( replicator.substitute( root ).replace( template, outdir ), replicator.substitute( d ) )
			os.mkdir( d_out )
			DirCounter = DirCounter + 1
		for f in files:
			f_in = os.path.join( root, f )
			f_out = os.path.join( replicator.substitute( root ).replace( template, outdir ), replicator.substitute( f ) )
			filename, filetype = os.path.splitext(f_in)
			if filetype in ['.xml', '.config', '.xcs', '.xcu', '.py', '.txt', '.xdl', '.xlb', '.properties', '.tree', '.xhp']:
				file_in=open(f_in, 'r')
				file_out=open(f_out, 'w')
				contents = file_in.read()
				file_out.write( replicator.substitute( contents ) )
			else:
				import shutil
				shutil.copyfile(f_in,f_out)
			FileCounter = FileCounter + 1
	print ('Project "%s" has successfully created with %s directories and %s files.' % (project, DirCounter, FileCounter))

if __name__ == '__main__':
	main()

