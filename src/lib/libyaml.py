## Cabecera X-Frame-Options para mejorar la seguridad
Header always append X-Frame-Options SAMEORIGIN
 
# Tell the browser to attempt the HTTPS version first
Header add Strict-Transport-Security "max-age=157680000"
 
## Cabecera X-XSS-Protection para evitar ataques XSS en IE y Chrome
Header set X-XSS-Protection "1; mode=block"
 
## Cabecera X-Content-Type-Options para evitar que se carguen hojas de estilo o scripts maliciosos
Header set X-Content-Type-Options "nosniff"
 
# Disable server signature
Header set ServerSignature "Off"
Header set ServerTokens "Prod"

import sys, sqlite3, os, inspect, json, yaml
from os.path import expanduser
from collections import OrderedDict


class LibYaml:
	def __init__(self, directory=expanduser("~/.betcon/config.yml")):
		self.directory = directory
		self.config = self.load()
		self.stake = self.config["stake"]

	def load(self):
		if not os.path.exists(self.directory):
			self.initConfig()

		stream = open(self.directory, 'r')
		config = yaml.load(stream)
		stream.close()
		return config

	def initConfig(self):
		data = {'stake': {'percentage': 1.0, 'stake': 0, 'type': 1}}

		stream = open(self.directory, 'w')
		yaml.dump(data, stream, default_flow_style=False)
		stream.close()

	def save(self):
		stream = open(self.directory, 'w')
		yaml.dump(self.config, stream, default_flow_style=False)
		stream.close()




