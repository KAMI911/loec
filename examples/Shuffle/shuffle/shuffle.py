try:
	# newer Pythons do not support relative imports, OOo Python does not seem to support absolute import
	import shuffle.extensioncore		# non-"from" import gives more relevant error message (see uno.py)
	from shuffle.extensioncore import *
except ImportError:
	import extensioncore			# non-"from" import gives more relevant error message (see uno.py)
	from extensioncore import *

SUPPORTED_LANGUAGES = ('en',)		# first one is default

com_sun_star_awt_SystemPointer_ARROW = uno.getConstantByName( 'com.sun.star.awt.SystemPointer.ARROW' )
com_sun_star_awt_SystemPointer_REFHAND = uno.getConstantByName( 'com.sun.star.awt.SystemPointer.REFHAND' )


from com.sun.star.awt import XMouseListener, XActionListener
class Shuffle( ComponentBase, XMouseListener, XActionListener ):
	SUPPORTED_LANGUAGES = SUPPORTED_LANGUAGES
	def firstrun( self ):
		self.addMenuItem( 'com.sun.star.sheet.SpreadsheetDocument', '.uno:Validation', 'Shuffle Rows', 'shuffle' )
		for t in documenttypes:
			try:    # some document types may not be available at all
				self.addMenuItem( t, '.uno:ExtendedHelp', self.localize( 'about' ), 'showabout' )
			except:
				debug( 'could not install help menu in ' + t )
				debugexception()
	def uninstall( self ):
		for t in documenttypes:
			try:    # some document types may not be available at all
				self.removeMenuItem( t, 'showabout' )
			except:
				debug( 'could not uninstall help menu in ' + t )
				debugexception()
		self.removeMenuItem( 'com.sun.star.sheet.SpreadsheetDocument', 'shuffle' )

	def shuffle( self ):
		selection = self.getcontroller().Selection
		debug( selection.getCellByPosition( 0, 0 ).Formula )
		def readrow( r ):
			for c in range( selection.Columns.Count ):
				yield selection.getCellByPosition( c, r ).Formula
		def writerow( r, contents ):
			for c in range( selection.Columns.Count ):
				selection.getCellByPosition( c, r ).Formula = contents[c]
		rows = [list( readrow( r ) ) for r in range( selection.Rows.Count )]
		import random
		random.shuffle( rows )
		for r in range( selection.Rows.Count ):
			writerow( r, rows[r] )

	def showabout( self ):
		self.dlg = dlg = self.createdialog( 'About' )
		if DEBUG:
			dlg.DebugButton.addActionListener( self )
		else:
			dlg.DebugButton.setVisible( False )
		dlg.Image.Model.ImageURL = unohelper.systemPathToFileUrl( self.path + '/logo_' + self.uilanguage + '.gif' )
		dlg.URL.addMouseListener( self )
		dlg.execute()
	def on_action_DebugButton( self ):
		self.dlg.endExecute()
		self.dlg = dlg = self.createdialog( 'ExtensionCreator' )
		dlg.ExecuteCode.addActionListener( self )
		dlg.SaveDialogs.addActionListener( self )
		self.updateOutputInCreatorDialog()
		dlg.execute()
	def updateOutputInCreatorDialog( self ):
		import sys
		if sys.platform in DEBUGFILEPLATFORMS:
			self.dlg.OutputField.Model.Text = file( debugfile, 'r' ).read()
			selection = uno.createUnoStruct( 'com.sun.star.awt.Selection' )
			selection.Min = selection.Max = len( self.dlg.OutputField.Model.Text )
			self.dlg.OutputField.Selection = selection
	def on_action_ExecuteCode( self ):
		try:
			code = self.dlg.CodeField.Model.Text
			exec code
		except:
			debugexception()
		self.updateOutputInCreatorDialog()
	def on_action_SaveDialogs( self ):
		try:
			import os
			dialogs = 'EOECShuffleDialogs'
			installed = os.path.join( self.path, dialogs )
			development = os.path.join( HOME, dialogs )
			for f in os.listdir( installed ):
				if f == 'RegisteredFlag': continue
				contents = file( os.path.join( installed, f ), 'rb' ).read()
				file( os.path.join( development, f ), 'wb' ).write( contents )
			debug( 'dialogs saved' )
		except:
			debugexception()
		self.updateOutputInCreatorDialog()
	# XActionListener
	def actionPerformed( self, event ):
		try:
			getattr( self, 'on_action_' + event.Source.Model.Name )()
		except:
			debugexception()
	# XMouseListener
	def mousePressed( self, event ):
		pass
	def mouseReleased( self, event ):
		try:
			shellexec = self.ctx.getServiceManager().createInstanceWithContext( 'com.sun.star.system.SystemShellExecute', self.ctx )
			shellexec.execute( self.localize( 'aboutURL' ), '', uno.getConstantByName( 'com.sun.star.system.SystemShellExecuteFlags.DEFAULTS' ) )
		except:
			debugexception()
	def mouseEntered( self, event ):
		try:
			peer = self.dlg.Peer
			pointer = self.ctx.getServiceManager().createInstance( 'com.sun.star.awt.Pointer' )
			pointer.setType( com_sun_star_awt_SystemPointer_REFHAND )
			peer.setPointer( pointer )
			for w in peer.Windows:
				w.setPointer( pointer )
		except:
			debugexception()
	def mouseExited( self, event ):
		try:
			peer = self.dlg.Peer
			pointer = self.ctx.getServiceManager().createInstance( 'com.sun.star.awt.Pointer' )
			pointer.setType( com_sun_star_awt_SystemPointer_ARROW )
			peer.setPointer( pointer )
			for w in peer.Windows:
				w.setPointer( pointer )
		except:
			debugexception()

init( Shuffle )
