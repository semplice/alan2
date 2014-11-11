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

import xml.etree.ElementTree as etree

class BaseObject(etree.Element):
	""" A BaseObject class is the base menu object.
	Items, Headers and Menus extends this class to generate a working object. """

	objectName = "BaseObject"

	def __init__(self):
		""" Initializes the object. """

		etree.Element.__init__(self, self.objectName)
	
	def set(self, key, value):
		"""
		Sets the key-value pair, ensuring that the value is properly
		decoded to utf-8
		"""
		
		return etree.Element.set(self, key, value.decode("utf-8"))

class DynamicObject(etree.Element):
	""" A BaseObject-derived object with the objectName set at runtime. """
	
	def __init__(self, name, text=None):
		""" Initializes the object.
		
		'name' is the object's name.
		'text', if not None, is the text to set. If None, no text will
		be set."""
		
		etree.Element.__init__(self, name)
		if text:
			self.text = text.decode("utf-8")

	def set(self, key, value):
		"""
		Sets the key-value pair, ensuring that the value is properly
		decoded to utf-8
		"""
		
		return etree.Element.set(self, key, value.decode("utf-8"))
