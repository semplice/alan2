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
# This file contains the IconPool object.

import os

def load():
	""" We do not want to waste time loading pieces of the GTK libraries
	when we are disabiling the icon support.
	Thus, this ugly workaround will be called on load by IconPool's __init__
	when the enabled parameter is set to True. """
	
	from gi.repository import Gtk, Gio
	
	global Gtk, Gio
	
class IconPool:
	""" A Pool of icons. """

	size = 96 # Ovverride this using the size argument on any function.
	
	def __init__(self, enabled):
		""" Initializes the object.
		
		If enabled is True, icon support will be enabled. """
		
		self.enabled = enabled
		
		if self.enabled:
			load()
			
			self.theme = Gtk.IconTheme.get_default()
	
	def __get_stock_icon(self, icon, size=size):
		""" Gets an icon from the GTK+ icons repository.
		Use get_icon() instead. It will call this def when needed. """
		
		if type(icon) not in (Gio.Icon, Gio.ThemedIcon, Gio.FileIcon):
			icon = self.theme.lookup_icon(icon.replace(".png","").replace(".xpm","").replace(".svg",""), self.size, 0)
		else:
			# Assuming it's gicon
			icon = self.theme.lookup_by_gicon(icon, self.size, 0)
		
		if icon:
			return icon.get_filename()
		else:
			return None

	def get_icon(self, icon, size=size):
		""" Examinates an icon, then returns an appropriate filename. """
		
		if not self.enabled or not icon: return None
		
		if type(icon) not in (Gio.Icon, Gio.ThemedIcon, Gio.FileIcon):
			
			icon = os.path.expanduser(icon)
		
			if icon[0] == "/":
				# local icon
				if os.path.exists(icon):
					return icon
				else:
					return None
		
		return self.__get_stock_icon(icon, self.size)
