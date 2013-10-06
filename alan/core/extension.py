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

import xdg.DesktopEntry
import sys
import xml.etree.ElementTree as etree

from alan.core.objects.menu import OpenboxMenu, Menu
from alan.core.objects.item import Item

class Extension(OpenboxMenu):
	""" A base Extension object. Extension should subclass this. """
	
	extensionName = "Extension"
	structure = []
	structure_links = {}
	
	def __init__(self, settings={}):
		""" Initializes the object. """
		
		self.extensionId = self.__module__.replace("alan.extensions.", "")
		
		self.settings = settings
		self.extension_settings = settings["extension:%s" % self.extensionId]
		
		if "structure" in self.extension_settings:
			self.structure = self.extension_settings["structure"].split(" ")
		
		OpenboxMenu.__init__(self)

		self.menu = Menu(self.extensionName)
		
		self.append(self.menu)
	
	def generate(self):
		""" By default, generate() will handle the structure and its relevant
		objects.
		You can tweak a structure item's creation by using the self.structure_links
		dictionary.
		
		You may of course override this method and handle everything by yourself. """
		
		for item in self.structure:
			
			# Get relevant link
			if item in self.structure_links:
				linkedto = self.structure_links[item]
			else:
				linkedto = None
			
			_item = item.split(":")
			if len(_item) > 1:
				# special object
				obj = _item[0]
				item = ":".join(_item[1:])
			else:
				# menu
				obj = "MenuLink"
				item = item
			
			# Properly set linkedto
			if not linkedto:
				if obj == "MenuLink":
					linkedto = self.new_menu_link
				elif obj == "ItemPool":
					linkedto = self.new_itempool
				elif obj == "Menu":
					linkedto = self.new_internal_menu
				elif obj == "LauncherPool":
					linkedto = self.new_launcher_pool
			
			linkedto(item)
		
	def new_launcher_pool(self, item):
		""" Creates a new LauncherPool """
		
		launcher_settings = self.settings["LauncherPool:%s" % item]
		structure = launcher_settings["structure"].split(" ")
		
		for item in structure:
			item_file = launcher_settings[item]
			item_file = xdg.DesktopEntry.DesktopEntry(item_file)
			
			self.add(Item(label=item_file.getName()))
	
	def new_menu_link(self, item):
		""" Creates a new_menu_link """
		
		self.add(Menu(id=item))
	
	def new_internal_menu(self, item):
		""" Creates a new internal menu """
		
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
