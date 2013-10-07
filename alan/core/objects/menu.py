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
# This file contains the Menu object.

from alan.core.objects.baseobject import BaseObject

class OpenboxMenu(BaseObject):
	""" The main Openbox menu tag. """

	objectName = "openbox_menu"

class Menu(BaseObject):
	""" A Menu class contains an openbox submenu. """
	
	objectName = "menu"
	
	def __init__(self, id, label=None, execute=None, icon=None):
		""" Initializes the object. """
		
		BaseObject.__init__(self)
		self.set("id", id)
		if label:
			self.set("label", label)
		if execute:
			self.set("execute", execute)
		if icon:
			self.set("icon", icon)
