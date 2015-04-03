# -*- coding: utf-8 -*-
#
# alan2 - An openbox menu builder
# Copyright (C) 2014  Semplice Project
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
#    Eugenio "g7" Paolantonio <me@medesimo.eu
#
# This file contains the logout (vera version) extension.

import os, sys

from gi.repository import Gio

from getpass import getuser

import alan.core.extension as extension
from alan.core.objects.separator import Header, Separator
from alan.core.objects.item import Item
from alan.core.objects.menu import Menu
from alan.core.objects.actions import ExecuteAction

userbegin = 1000

USER = getuser()
HOME = os.path.expanduser("~")

# ExitAction "enum"
ExitAction = {
	0 : None,
	1 : _("Power Off"),
	2 : _("Reboot"),
	3 : _("Suspend"),
	4 : _("Logout"),
	5 : _("Lock Screen"),
	6 : _("Hibernate"),
	7 : _("Switch User")
}

class Extension(extension.Extension):
	
	extensionName = "logout_vera"
	
	def generate(self):
		""" Actually generate things. """

		### Begin!
		
		settings = Gio.Settings("org.semplicelinux.vera")
		if settings.get_boolean("ninja-shortcut"):
			last = ExitAction[settings.get_enum("last-exit-action")]
		else:
			last = None

		# Add that choice!
		if last:
			choice = last + " " + _("(CTRL+ALT+SPACE)")
			self.add(self.return_executable_item(choice, "vera-command --ninja-shortcut", icon="favorites"))
			self.add(Separator())

		# Add normal choices
			
		# Lock screen
		self.add(self.return_executable_item(_("Lock Screen"), "vera-command --lock", icon="system-lock-screen"))
		# Logout
		self.add(self.return_executable_item(_("Logout"), "vera-command --logout", icon="system-log-out"))
		
		# Switch User
		# create menu:
		switch_items = Menu("switchuser_vera", _("Switch User"), icon=self.IconPool.get_icon("system-users"))
		# open passwd and populate switch_items
		at_least_one = False
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
					at_least_one = True
					_uhome = line[5]
					if os.path.exists(os.path.join(_uhome, ".face")):
						_uface = os.path.join(_uhome, ".face")
					else:
						_uface = "system-users"
				
					switch_items.append(self.return_executable_item(_udesc, "vera-command --switch-to-user " + _uname, icon=_uface))

		switch_items.append(Separator())
		switch_items.append(self.return_executable_item(_("Other..."), "vera-command --switch-user", icon="gdm"))
		
		if at_least_one:
			self.add(switch_items)
		else:
			# Generic switch user command
			self.return_executable_item(_("Switch User"), "vera-command --switch-user", icon="system-users")

		self.add(Separator())

		# Suspend
		self.add(self.return_executable_item(_("Suspend"), "vera-command --suspend", icon="system-suspend"))

		# Hibernate
		self.add(self.return_executable_item(_("Hibernate"), "vera-command --hibernate", icon="system-hibernate"))

		self.add(Separator())

		# Shutdown
		self.add(self.return_executable_item(_("Shutdown"), "vera-command --poweroff", icon="system-shutdown"))

		# Reboot
		self.add(self.return_executable_item(_("Reboot"), "vera-command --reboot", icon="system-reboot"))


	def return_executable_item(self, label, target, icon=None):
		""" Returns an executable item. """
				
		item = Item(label=label, icon=self.IconPool.get_icon(icon))
		action = ExecuteAction(target)
		item.append(action)
		
		return item
