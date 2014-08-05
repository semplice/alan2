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

import gmenu, re, sys
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
if os.path.exists("/usr/bin/oneslip"):
	ONESLIP = True
else:
	ONESLIP = False

to_skip = ("Administration", "Preferences")

class Extension(extension.Extension):
	
	extensionName = "xdgmenu"
	
	def walk(self, parent, menu=None):
		""" Walks through the menu and does pretty things. """

		for entry in parent:
			if entry.get_type() == gmenu.TYPE_DIRECTORY:
				if entry.menu_id in to_skip:
					continue
				
				# Directory, create new submenu
				_menu = Menu(escape(entry.menu_id), entry.name, icon=self.IconPool.get_icon(entry.icon))
				
				self.walk(entry.get_contents(), _menu)
				
				if menu is not None:
					menu.append(_menu)
				else:
					self.add(_menu)
				
			elif entry.get_type() == gmenu.TYPE_ENTRY and not entry.is_excluded:
					
				command = re.sub(' [^ ]*%[fFuUdDnNickvm]', '', entry.get_exec())
				if "oneslip" in command and not ONESLIP:
					# oneslip not installed, link to bricks
					command = "pkexec /usr/bin/bricks \"%s\" oneslip" % escape(entry.name.replace("&","and"))
				if entry.launch_in_terminal:
					command = 'x-terminal-emulator --title "%s" -e %s' % \
						(entry.name.replace("&","and"), command)
				
				menu.append(self.return_executable_item(entry.name, command, icon=entry.icon))

	def generate(self):
		""" Actually generate things. """

		if "hide_settings_menu" in self.extension_settings and self.extension_settings["hide_settings_menu"]:
			self.hide_settings_menu = True
		else:
			self.hide_settings_menu = False

		# Lookup menu file
		if "XDG_MENU_PREFIX" in os.environ and os.path.exists(
			os.path.join("/etc/xdg/menus", "%s-applications.menu" % os.environ["XDG_MENU_PREFIX"])
		):
			applications_menu = "%s-applications.menu" % os.environ["XDG_MENU_PREFIX"]
		else:
			applications_menu = "applications.menu" # Force to applications.menu, may fail if not existent, of course.

		# Walk through the normal Applications menu
		self.walk(gmenu.lookup_tree(applications_menu).get_directory_from_path("/").get_contents())
		
		if not self.hide_settings_menu:
			self.add(Separator())
			
			# Preferences
			preferences = gmenu.lookup_tree(applications_menu).get_directory_from_path("/System/Preferences")
			preferences_menu = Menu(escape(preferences.menu_id), escape(preferences.name), icon=self.IconPool.get_icon(preferences.icon))
			self.walk(preferences.get_contents(), preferences_menu)
			self.add(preferences_menu)
			
			# Administration
			administration = gmenu.lookup_tree(applications_menu).get_directory_from_path("/System/Administration")
			administration_menu = Menu(escape(administration.menu_id), escape(administration.name), icon=self.IconPool.get_icon(administration.icon))
			self.walk(administration.get_contents(), administration_menu)
			self.add(administration_menu)
		
	def return_executable_item(self, label, command, icon=None):
		""" Returns an executable item. """
		
		item = Item(label=label, icon=self.IconPool.get_icon(icon))
		action = ExecuteAction(command)
		item.append(action)
		
		return item
