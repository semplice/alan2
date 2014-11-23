# -*- coding: utf-8 -*-
#
# alan2 - An openbox menu builder
# Copyright (C) 2013  Semplice Project
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
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
# This file contains the xdgmenu extension.

#### BASED ON xdg-menu.py from fedora
#
# Copyright (C) 2008  Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Author(s): Luke Macken <lmacken@redhat.com>
#            Miroslav Lichvar <mlichvar@redhat.com>
####

import sys, os
import glob

from gi.repository import GMenu

import re, sys
from xml.sax.saxutils import escape

from getpass import getuser

import alan.core.extension as extension
from alan.core.objects.separator import Header, Separator
from alan.core.objects.item import Item
from alan.core.objects.menu import Menu
from alan.core.objects.actions import ExecuteAction

USER = getuser()
HOME = os.path.expanduser("~")

# Check for oneslip
#if os.path.exists("/usr/bin/oneslip"):
#	ONESLIP = True
#else:
#	ONESLIP = False

class Extension(extension.Extension):
	
	extensionName = "xdgmenu"
	
	def walk(self, parent, menu=None):
		""" Walks through the menu and does pretty things. """

		itr = parent.iter()
		typ = None
		
		while typ != GMenu.TreeItemType.INVALID:
			typ = itr.next()
						
			if typ == GMenu.TreeItemType.DIRECTORY:
				
				entry = itr.get_directory()
				
				if entry.get_menu_id() in self.to_skip or entry.get_is_nodisplay():
					continue
				
				# Directory, create new submenu
				_menu = Menu(escape(entry.get_menu_id()), entry.get_name(), icon=self.IconPool.get_icon(entry.get_icon()))
				
				self.walk(itr.get_directory(), _menu)
				
				if menu is not None:
					menu.append(_menu)
				else:
					self.add(_menu)
				
			elif typ == GMenu.TreeItemType.ENTRY:

				entry = itr.get_entry().get_app_info()
				if entry.get_is_hidden():
					continue
				
				name = entry.get_name()
					
				command = re.sub(' [^ ]*%[fFuUdDnNickvm]', '', entry.get_executable())
				#if "oneslip" in command and not ONESLIP:
				#	# oneslip not installed, link to bricks
				#	command = "pkexec /usr/bin/bricks \"%s\" oneslip" % escape(name.replace("&","and"))
				if entry.has_key("Terminal") and entry.get_boolean("Terminal"):
					command = 'x-terminal-emulator --title "%s" -e %s' % \
						(name.replace("&","and"), command)
				
				menu.append(self.return_executable_item(name, command, icon=entry.get_icon()))

	def generate(self):
		""" Actually generate things. """
		
		if "hide_settings_menu" in self.extension_settings and self.extension_settings["hide_settings_menu"]:
			self.hide_settings_menu = True
			self.to_skip = ()			
		else:
			self.hide_settings_menu = False
			self.to_skip = ("Administration", "Preferences")

		# Lookup menu file
		if "XDG_MENU_PREFIX" in os.environ and os.path.exists(
			os.path.join("/etc/xdg/menus", "%s-applications.menu" % os.environ["XDG_MENU_PREFIX"])
		):
			applications_menu = "%s-applications.menu" % os.environ["XDG_MENU_PREFIX"]
		else:
			applications_menu = "applications.menu" # Force to applications.menu, may fail if not existent, of course.

		# Walk through the normal Applications menu
		tree = GMenu.Tree.new(applications_menu, GMenu.TreeFlags.NONE);
		tree.load_sync()
		self.walk(tree.get_root_directory())
		
		if not self.hide_settings_menu:
			self.add(Separator())
			
			# Preferences
			preferences = tree.get_directory_from_path("/System/Preferences")
			preferences_menu = Menu(escape(preferences.get_menu_id()), escape(preferences.get_name()), icon=self.IconPool.get_icon(preferences.get_icon()))
			self.walk(preferences, preferences_menu)
			self.add(preferences_menu)
			
			# Administration
			administration = tree.get_directory_from_path("/System/Administration")
			administration_menu = Menu(escape(administration.get_menu_id()), escape(administration.get_name()), icon=self.IconPool.get_icon(administration.get_icon()))
			self.walk(administration, administration_menu)
			self.add(administration_menu)
		
	def return_executable_item(self, label, command, icon=None):
		""" Returns an executable item. """
		
		item = Item(label=label, icon=self.IconPool.get_icon(icon))
		action = ExecuteAction(command)
		item.append(action)
		
		return item
