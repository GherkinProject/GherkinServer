import ConfigParser
import json
import os

ad = os.path.abspath( __file__ )
ad = ad.rsplit('/', 1)[0] +'/'

class cfg_server:
	def __init__(self, fileName):
		self.fileName = fileName		
		self.config = ConfigParser.ConfigParser()

		#loading file				
		self.config.read(fileName)

		#================================================
		# Loading constants
		#================================================

		try:
			#extensions
			self.defaultFileExt = set(json.loads(self.config.get('extension', 'file')))
			self.defaultTagKept = set(json.loads(self.config.get('extension', 'tag')))
			self.defaultUnknown = self.config.get('extension', 'unk')

			#server port
			self.defaultPort = self.config.getint('server', 'port')
			self.serverName = self.config.get('server', 'name')

			#time
			self.dtCheck = self.config.getfloat('time', 'check')
			self.anticipateCheck = self.config.getfloat('time', 'anticipateCheck')

			#constante mode
			self.normal = self.config.getint('constante','normal')
			self.random = self.config.getint('constante','random')
			self.playlist = self.config.getint('constante','playlist')

			# pruning constant
			self.epsilon = self.config.getfloat('pruning','constante')

			#icon and locations
			self.root = self.config.get('location','root')
			self.dbMarkov = self.config.get('location','Markov')
			self.logLocation = self.config.get('location','log',0)
			self.defaultDbLocation = self.config.get('location','DbLoc',0)
			self.defaultDbFile = self.config.get('location','DbFile')
		except:
			#if no file was created, creates it
			self.reset()
			self.write()
			self.__init__(fileName)
		
	def reset(self):
		"""Reset Gherkin to Default configuration"""
		self.config.add_section('extension')
		self.config.set('extension', 'file', json.dumps([".mp3", ".ogg", ".flac"]))
		self.config.set('extension', 'tag', json.dumps(["artist", "album", "title", "date", "tracknumber", "genre"]))
		self.config.set('extension', 'unk', 'unknown')

		self.config.add_section('server')
		self.config.set('server', 'port', '1664')
		self.config.set('server', 'name', 'localhost')

		self.config.add_section('time')
		self.config.set('time', 'check', '1.0')
		self.config.set('time', 'anticipateCheck', '1.1')

		self.config.add_section('constante')
		self.config.set('constante', 'normal', '0')
		self.config.set('constante', 'random', '1')
		self.config.set('constante', 'playlist', '2')

		self.config.add_section('pruning')
		self.config.set('pruning', 'constante', '0.001')

		self.config.add_section('location')
		self.config.set('location', 'root', ad)
		self.config.set('location', 'log', '%(root)slog/')
		self.config.set('location', 'DbLoc', '%(root)s')
		self.config.set('location', 'Markov', 'dbMarkov.ghk')
		self.config.set('location', 'DbFile', 'db.xml')

	def set(self, section, name, value):
		"""Modify constant in file and in instance"""
		self.config.set(section, name, value)
		self.write()
		self.__init__(self.fileName)

	def write(self):
		"""Write the actual configuration in the file "name" """
		with open(self.fileName, 'wb') as configfile:
			self.config.write(configfile)

config = cfg_server(ad + 'configServer.cfg')
