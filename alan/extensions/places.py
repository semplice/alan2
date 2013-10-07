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
# This file contains the places extension.

import t9n.library

import os

from getpass import getuser

import alan.core.extension as extension
from alan.core.objects.separator import Header, Separator
from alan.core.objects.item import Item
from alan.core.objects.menu import Menu
from alan.core.objects.actions import ExecuteAction

_ = t9n.library.translation_init("alan2")

USER = getuser()
HOME = os.path.expanduser("~")

class Extension(extension.Extension):
	
	extensionName = "places"
	
	def generate(self):
		""" Actually generate things. """
		
		if "filemanager" in self.extension_settings:
			self.filemanager = self.extension_settings["filemanager"]
		else:
			self.filemanager = "pcmanfm --new-win"
		
		# User's home directory
		self.add(self.return_executable_item(USER, "file://%s" % HOME, icon="user-home"))
		
		# Desktop
		self.add(self.return_executable_item(_("Desktop"), "file://%s" % os.path.join(HOME, "Desktop"), icon="user-desktop"))
		
		# Trash
		self.add(self.return_executable_item(_("Trash"), "trash://", icon="user-trash"))

		# Computer
		self.add(self.return_executable_item(_("Computer"), "computer://", icon="computer"))
		
		# Separator
		self.add(Separator())
		
		## MEDIA

		# Root (/)
		self.add(self.return_executable_item(_("System (/)"), "file:///", icon="drive-harddisk"))

		with open("/proc/mounts") as mounts:

			# Other items listed in /media
			for media in mounts.readlines():
				if "/media" in media:
					
					if "iso9660" in media or "udf" in media:
						# It is a CD. Maybe.
						icon = "media-optical"
					else:
						icon = "drive-harddisk"
					
					# Is on media. Yay.
					dire = media.split(" ")[1].replace('\\040'," ") # use only the directory name
					self.add(self.return_executable_item(os.path.basename(dire).replace("_","__"), dire, icon=icon))

		if os.path.exists(os.path.join(HOME, ".gtk-bookmarks")):
			self.add(Separator())

			with open(os.path.join(HOME, ".gtk-bookmarks")) as _file:
				for line in _file:
					line = line.split(" ")
					directory = line[0].replace("\n","")
					if len(line) > 1:
						name = " ".join(line[1:]).replace("_","__").replace("\n","")
					else:
						name = os.path.basename(directory.replace("file://","")).replace("_","__").replace("\n","")
					if directory.startswith("smb://"):
						icon = "folder-remote-smb"
					elif directory.startswith("nfs://"):
						icon = "folder-remote-nfs"
					elif directory.startswith("ssh://"):
						icon = "folder-remote-ssh"
					elif directory.startswith("ftp://"):
						icon = "folder-remote-ftp"
					else:
						icon = "folder"
					self.add(self.return_executable_item(name, directory, icon=icon))
		
	def return_executable_item(self, label, target, icon=None):
		""" Returns an executable item. """
		
		item = Item(label=label, icon=icon)
		action = ExecuteAction("%s \"%s\"" % (self.filemanager, target))
		item.append(action)
		
		return item
