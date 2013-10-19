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
# This file contains the main extension.

from getpass import getuser
from socket import gethostname

import xdg.DesktopEntry

import os, sys

import alan.core.extension as extension
from alan.core.objects.separator import Header, Separator
from alan.core.objects.item import Item
from alan.core.objects.menu import Menu
from alan.core.objects.actions import ExecuteAction

HeaderMagic = {"__username__":getuser(), "__hostname__":gethostname()}

class Extension(extension.Extension):
	
	extensionName = "main"
	
	def generate(self):
		""" Actually generate things. """
		
		if self.extension_settings["show_header"]:
			header_text = self.extension_settings["header_text"]
			if header_text in HeaderMagic:
				header_text = HeaderMagic[header_text]

			self.add(Header(header_text))
		
		result = self.parse_structure()
		for item in result: self.add(item)
	
	def parse_structure(self, structure=None):
		""" Parses the defined structure. If structure is None, self.structure
		will be used.
		
		Returns a list with the items to add to the main menu."""
	
		if not structure: structure = self.structure
		returnlst = []

		# Get special objects...
		for item in structure:
			if (item.startswith("ItemPool") or item.startswith("Menu") or item.startswith("LauncherPool")) and not item in self.settings:
				# obtain settings!
				self.configuration.populate_settings(item)
		self.settings = self.configuration.settings # update settings

		for item in structure:
			
			if item == "-":
				# It's a separator!
				returnlst.append(Separator())
				continue
			
			_item = item.split(":")
			if len(_item) > 1:
				# special object
				obj = _item[0]
				item = ":".join(_item[1:])
			else:
				# menu
				obj = "MenuLink"
				item = item
			
			# Set linkedto
			if obj == "MenuLink":
				linkedto = self.new_menu_link
			elif obj == "ItemPool":
				linkedto = self.new_itempool
			elif obj == "Menu":
				linkedto = self.new_internal_menu
			elif obj == "LauncherPool":
				linkedto = self.new_launcher_pool
			
			returnlst += linkedto(item)
		
		return returnlst
		
	def new_launcher_pool(self, item):
		""" Creates a new LauncherPool """
		
		returnlst = []
		
		launcher_settings = self.settings["LauncherPool:%s" % item]
		structure = launcher_settings["structure"].split(" ")
		
		for item in structure:
			item_file = launcher_settings[item]
			item_file = xdg.DesktopEntry.DesktopEntry(item_file)
			
			item = Item(label=item_file.getName())
			# Create an action...
			action = ExecuteAction(item_file.getExec())
			
			item.append(action)
			
			returnlst.append(item)
		
		return returnlst
	
	def new_menu_link(self, item):
		""" Creates a new_menu_link """
		
		if self.is_pipe:
			execute = "%s %s" % (os.path.abspath(sys.argv[0]), item)
		else:
			execute = None
		
		# Get name
		if "label_%s" % item in self.extension_settings:
			label = self.extension_settings["label_%s" % item]
		else:
			label = None
		
		return [Menu(id=item, label=label, execute=execute), ]
			
	def new_internal_menu(self, item):
		""" Creates a new internal menu """
		
		returnlst = []
		
		# Get structure
		menu_settings = self.settings["Menu:%s" % item]
		structure = menu_settings["structure"].split(" ")

		# Get name
		if "label_%s" % item in self.extension_settings:
			label = self.extension_settings["label_%s" % item]
		elif "label_%s" % item in menu_settings:
			label = menu_settings["label_%s" % item]
		else:
			label = None

		# Create containing menu
		menu = Menu(id=item, label=label)
		
		result = self.parse_structure(structure)
		for item in result: menu.append(item)
		
		return [menu,]
	
	def new_itempool(self, item):
		""" Creates a new ItemPool. """
		
		return []
