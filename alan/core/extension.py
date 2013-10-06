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
# This file contains the BaseObject.

import sys
import xml.etree.ElementTree as etree

from alan.core.objects.menu import OpenboxMenu, Menu

class Extension(OpenboxMenu):
	""" A base Extension object. Extension should subclass this. """
	
	extensionName = "Extension"
	structure = []
	
	def __init__(self, configuration=None):
		""" Initializes the object. """
		
		self.extensionId = self.__module__.replace("alan.extensions.", "")
		
		self.configuration = configuration
		self.settings = configuration.settings
		self.extension_settings = self.settings["extension:%s" % self.extensionId]
		
		if "structure" in self.extension_settings:
			self.structure = self.extension_settings["structure"].split(" ")
		
		OpenboxMenu.__init__(self)

		self.menu = Menu(self.extensionName)
		
		self.append(self.menu)
	
	def generate(self):
		""" Override this method to actually do things. """
		
		pass
	
	def add(self, obj):
		""" Appends to the main menu the specified object. """
		
		return self.menu.append(obj)
	
	def get_menu(self):
		""" Prints the resulting menu. """
		
		etree.ElementTree(self).write(sys.stdout)
	
	def write_menu(self, dest):
		""" Writes the menu in dest."""
		
		etree.ElementTree(self).write(dest)
