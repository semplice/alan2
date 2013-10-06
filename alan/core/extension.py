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
	
	def __init__(self):
		""" Initializes the object. """
		
		OpenboxMenu.__init__(self)

		self.menu = Menu(self.extensionName)
		
		self.append(self.menu)
	
	def generate(self):
		""" Extension creators should override this method to get things
		done. """
		
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
