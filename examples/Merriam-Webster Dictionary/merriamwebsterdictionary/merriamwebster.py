import util.web

def getmeanings( word ):
	root = 'http://www.merriam-webster.com'
	url = root + '/dictionary/' + word
	html = util.web.getpage( url )
	from BeautifulSoup import BeautifulSoup
	soup = BeautifulSoup( html )
	meanings = []
	for s in soup.find( 'ol', attrs={'class': 'results'} ).findAll( 'li' ):
		sup = s.find( 'sup' )
		if sup is None:
			continue
		a = s.find( 'a' )
		meanings.append( (root + a['href'], a.contents[1]) )
	return meanings

def lookup( url ):
	html = util.web.getpage( url )
	from BeautifulSoup import BeautifulSoup
	soup = BeautifulSoup( html )
	defs = soup.find( 'div', attrs={'class': 'defs'} )
	definitions = []
	for content in defs.findAll( 'span', attrs={'class': 'sense_content' } ):
		definition = util.web.flatten( content )
		if definition.startswith( ':' ):
			definition = definition[1:]
		definition = definition.strip()
		definition = definition.replace( '&lt;', '<' )
		definition = definition.replace( '&gt;', '>' )
		definitions.append( definition )
	return definitions

def main():
	import sys
	try:
		print getmeanings( sys.argv[1] )
	except:
		print lookup( sys.argv[1] )

if __name__ == '__main__':
	main()

 