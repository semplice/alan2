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
#    Giuseppe `GsC_RuL3Z` Corti <giuseppe@infiniteloop.pro>
#
# This file contains the places extension.

import os

from getpass import getuser

import alan.core.extension as extension
from alan.core.objects.separator import Separator
from alan.core.objects.item import Item
from alan.core.objects.menu import Menu
from alan.core.objects.actions import ExecuteAction

USER = getuser()
HOME = os.path.expanduser("~")

class Extension(extension.Extension):
	
	extensionName = "appearance"
	
	def generate(self):
		""" Actually generate things. """

		# Wallpapers submenu
		_menu = Menu("wallpaper", _("Wallpaper"), icon=self.IconPool.get_icon("preferences-desktop-wallpaper"))
		_menu.append(self.return_executable_item(_("Add"), "nitrogen-add-wallpaper", icon="gtk-add"))
		_menu.append(self.return_executable_item(_("Manage"), "nitrogen", icon="preferences-desktop-wallpaper"))

		self.add(_menu)
		self.add(Separator())
		
		# Theme selector
		self.add(self.return_executable_item(_("Appearance settings"), "lxappearance", icon="preferences-desktop-theme"))
		
		# Paranoid
		if os.path.exists("/usr/bin/paranoid"):
			self.add(self.return_executable_item(_("Visual effects"), "paranoid", icon="desktop-effects"))

		
		
	def return_executable_item(self, label, target, icon=None):
		""" Returns an executable item. """
		
		item = Item(label=label, icon=self.IconPool.get_icon(icon))
		action = ExecuteAction(target)
		item.append(action)
		
		return item
