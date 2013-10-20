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
from alan.core.objects.icon import IconPool

class Extension(OpenboxMenu):
	""" A base Extension object. Extension should subclass this. """
	
	extensionName = "Extension"
	structure = []
	
	def __init__(self, configuration=None, is_pipe=False):
		""" Initializes the object. """
		
		self.is_pipe = is_pipe
		
		self.extensionId = self.__module__.replace("alan.extensions.", "")
		
		self.configuration = configuration
		self.settings = configuration.settings
		if "extension:%s" % self.extensionId in self.settings:
			self.extension_settings = self.settings["extension:%s" % self.extensionId]
		else:
			self.extension_settings = {}
		
		if "structure" in self.extension_settings:
			self.structure = self.extension_settings["structure"].split(" ")
		
		if not "icons" in self.settings["alan"]:
			icons = False
		else:
			icons = self.settings["alan"]["icons"]
		
		self.IconPool = IconPool(icons)
		
		if is_pipe:
			# pipemenu, change things accordingly
			self.objectName = "openbox_pipe_menu"

		OpenboxMenu.__init__(self)

		if not is_pipe:
			if self.settings["alan"]["map_as_main"] == self.extensionId:
				self.menu = Menu("root-menu")
				self.menu.set("label", "Openbox 3")
			else:
				self.menu = Menu(self.extensionName)
				
				# Unfortunately in non-pipe mode Openbox gets the label from
				# the menu file and not from the id link in the main menu.
				# We need then to get the label.
				main = "extension:%s" % self.settings["alan"]["map_as_main"]
				self.configuration.populate_settings(main)
				
				if not "%s_label" % self.extensionName:
					label = "alan2"
				else:
					label = self.configuration.settings[main]["%s_label" % self.extensionName]
				
				self.menu.set("label", label)
				
			

			self.set("xmlns", "http://openbox.org/")
			self.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
			self.set("xsi:schemaLocation", "http://openbox.org/ file:///usr/share/openbox/menu.xsd")
			
			self.append(self.menu)
	
	def generate(self):
		""" Override this method to actually do things. """
		
		pass
	
	def add(self, obj):
		""" Appends to the main menu the specified object. """
		
		if self.is_pipe:
			return self.append(obj)
		else:
			return self.menu.append(obj)
	
	def get_menu(self):
		""" Prints the resulting menu. """
		
		etree.ElementTree(self).write(sys.stdout)
	
	def write_menu(self, dest):
		""" Writes the menu in dest."""
		
		etree.ElementTree(self).write(dest, encoding='utf-8', xml_declaration=True)
