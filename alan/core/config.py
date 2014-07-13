# -*- coding: utf-8 -*-
#
# alan2 - An openbox menu builder
# Copyright (C) 2013  Semplice Project
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# Authors:
#    Eugenio "g7" Paolantonio <me@medesimo.eu>
#
# This file parses a configuration file.

import ConfigParser as cp
import os

DEFAULTS = "/etc/alan/alan.conf"
USER = os.path.expanduser("~/.config/alan/alan.conf")

class Configuration(cp.SafeConfigParser):
	""" The Configuration() class handles a configuration file. """
	
	settings = {}
	
	def __init__(self, extension, directory, profile=None):
		""" Initializes the object.
		
		extension is the extension to parse. """
		
		cp.SafeConfigParser.__init__(self)
		
		if profile:
			DEFAULTS = "/etc/alan/alan-%s.conf" % profile
			USER = os.path.join(directory, "alan/alan-%s.conf" % profile)
		else:
			DEFAULTS = "/etc/alan/alan.conf"
			USER = os.path.join(directory, "alan/alan.conf")
				
		# Load DEFAULTS and USER
		self.read((DEFAULTS, USER))
		
		# Populate settings with the application settings...
		self.populate_settings("alan")
		
		# ...and for the extension.
		if "extension:%s" % extension in self.sections():
			self.populate_settings("extension:%s" % extension)
		
	def populate_settings(self, extension):
		""" Populates self.settings with extension's settings. """
		
		self.settings[extension] = {"__ConfigParser":self}
		for option, value in self.items(extension):
			# Handle boolean values and None
			if value.lower() == "false":
				value = False
			elif value.lower() == "true":
				value = True
			elif value.lower() == "none":
				value = None
			
			if "label" in option:
				value = _(value)
			
			self.settings[extension][option] = value
		
