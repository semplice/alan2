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

import t9n.library

import os, sys
import ConfigParser as cp

from getpass import getuser

import alan.core.extension as extension
from alan.core.objects.separator import Header, Separator
from alan.core.objects.item import Item
from alan.core.objects.menu import Menu
from alan.core.objects.actions import ExecuteAction

_ = t9n.library.translation_init("alan2")

userbegin = 1000


USER = getuser()
HOME = os.path.expanduser("~")
cfile = os.path.join(HOME, ".semplice-logout")


class Extension(extension.Extension):
	
	extensionName = "logout"
	
	def generate(self):
		""" Actually generate things. """

		### Begin!

		sort = ("lock", "logout", "switch", "suspend", "hibernate", "shutdown", "reboot") # Workaround that has to be made after switching from numbers to words.
		
		actions = {"lock":_("Lock Screen"), "logout":_("Logout"), "switch":_("Switch User"), "switch_guest":_("Guest session"), "suspend":_("Suspend"), "hibernate":_("Hibernate"), "shutdown":_("Shutdown"), "reboot":_("Reboot")}
		ections = {"lock":"semplice-logout --lock", "logout":"semplice-logout --logout", "switch":"semplice-logout --switch-user", "switch_guest":"semplice-logout --switch-to-guest", "suspend":"semplice-logout --suspend", "hibernate":"semplice-logout --hibernate", "shutdown":"semplice-logout --shutdown","reboot":"semplice-logout --reboot"}
		ictions = {"lock":"system-lock-screen", "logout":"system-log-out", "switch":"system-users", "switch_guest":"system-users", "suspend":"gnome-session-suspend", "hibernate":"gnome-session-hibernate", "shutdown":"gnome-session-halt", "reboot":"gnome-session-reboot"}

		# After <robo>, add a separator.
		sep = ("switch", "hibernate")

		# Read configuration file
		if os.path.exists(cfile):
			cfg = cp.SafeConfigParser()
			cfg.read(cfile)
				
			# Get last choice
			last = cfg.get("Last","last_action")
			if last.lower() == "none": last = False
		else:
			last = False

		# Add that choice!
		if last:
			choice = actions[last] + " " + _("(CTRL+ALT+SPACE)")
			self.add(self.return_executable_item(choice, ections[last], icon=self.IconPool.get_icon(ictions[last])))
			self.add(Separator())

		# Add normal choices
			
		# Lock screen
		self.add(self.return_executable_item("Lock Screen", "semplice-logout --lock", icon=self.IconPool.get_icon("system-lock-screen")))
		# Logout
		self.add(self.return_executable_item("Logout", "semplice-logout --logout", icon=self.IconPool.get_icon("system-log-out")))
		
		# Switch User
		# create menu:
		switch_items = []
		# open passwd and populate switch_items
		with open("/etc/passwd", "r") as passwd:
			for line in passwd.readlines():
				line = line.split(":")
				_uid = int(line[2])
				if _uid < userbegin or _uid == 65534:
					continue # Skip users < userbegin and 65534 (nobody)
				
				_uname = line[0]
				_udesc = line[4].split(",")[0]
				if not _udesc: _udesc = _uname
				
				if not _uname == USER:
					_uhome = line[5]
					if os.path.exists(os.path.join(_uhome, ".face")):
						_uface = os.path.join(_uhome, ".face")
					else:
						_uface = "system-users"
				
					switch_items.append(self.return_executable_item(_udesc, "semplice-logout --switch-to " + _uname, icon=self.IconPool.get_icon(_uface)))
				else:
					_uface = "gnome-settings-default-applications"

					_menu = Menu("usermenu", _udesc, icon=self.IconPool.get_icon(_uface))
					_menu.append(self.return_executable_item("Change profile image", "semplice-change-face", icon=self.IconPool.get_icon("eog")))

					switch_items.append(_menu)

		switch_items.append(Separator())
		switch_items.append(self.return_executable_item("Other...", "semplice-logout --switch-user", icon=self.IconPool.get_icon("gdm")))

		self.add(Menu("switchuser", "Switch menu", icon=self.IconPool.get_icon("system-users")))
		

		self.add(Separator())

		# Suspend
		self.add(self.return_executable_item("Suspend", "semplice-logout --suspend", icon=self.IconPool.get_icon("gnome-session-suspend")))

		# Hibernate
		self.add(self.return_executable_item("Hibernate", "semplice-logout --hibernate", icon=self.IconPool.get_icon("gnome-session-hibernate")))

		self.add(Separator())

		# Shutdown
		self.add(self.return_executable_item("Shutdown", "semplice-logout --shutdown", icon=self.IconPool.get_icon("gnome-session-halt")))

		# Reboot
		self.add(self.return_executable_item("Reboot", "semplice-logout --reboot", icon=self.IconPool.get_icon("gnome-session-reboot")))

		self.add(Separator())

		# Settings
		self.add(self.return_executable_item("Settings...", "semplice-logout --settings", icon=self.IconPool.get_icon("preferences-desktop")))


	def return_executable_item(self, label, target, icon=None):
		""" Returns an executable item. """
		
		item = Item(label=label, icon=self.IconPool.get_icon(icon))
		action = ExecuteAction(target)
		item.append(action)
		
		return item
