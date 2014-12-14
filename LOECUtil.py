class LOECUtil:

	def __init__(self, project, vendor, prefix, url, loecurl):
		self.project=project
		self.vendor=vendor
		self.prefix=prefix
		self.url=url
		self.loecurl=loecurl
	
	def substitute(self, text ):
		text = text.replace( '%Extension Name%', self.project )
		text = text.replace( '%Vendor Name%', self.vendor )
		for separator in ('', '-', '_'):
			id = self.project
			for sep in (' ', '-', '_', '.', ','):
				id = id.replace( sep, separator )
			text = text.replace( '%Extension' + separator + 'Name%', id )
			text = text.replace( '%extension' + separator + 'name%', id.lower() )
			id = self.vendor
			for sep in (' ', '-', '_', '.', ','):
				id = id.replace( sep, separator )
			text = text.replace( '%Vendor' + separator + 'Name%', id )
			text = text.replace( '%vendor' + separator + 'name%', id.lower() )
		text = text.replace( '%prefix%', self.prefix )
		text = text.replace( '%url%', self.url )
		text = text.replace( '%Creator Name%', 'LibreOffice Extension Creator (by KAMI) based on EuroOffice Extension Creator (by MultiRacio Ltd.)' )
		text = text.replace( '%Creator Short Name%', 'LibreOffice Extension Creator' )
		text = text.replace( '%creator url%', self.loecurl )
		return text

