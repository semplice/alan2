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
# This file contains some helpers for etree.

import xml.etree.ElementTree as etree

class PIParser(etree.XMLTreeBuilder):
	""" Parser which handles comments, too. 
	
	Taken from http://effbot.org/zone/element-pi.htm
	"""

	def __init__(self):
		 etree.XMLTreeBuilder.__init__(self)
		 # assumes ElementTree 1.2.X
		 self._parser.CommentHandler = self.handle_comment
		 self._parser.ProcessingInstructionHandler = self.handle_pi
		 self._target.start("document", {})

	def close(self):
		 self._target.end("document")
		 return etree.XMLTreeBuilder.close(self)

	def handle_comment(self, data):
		 self._target.start(etree.Comment, {})
		 self._target.data(data)
		 self._target.end(etree.Comment)

	def handle_pi(self, target, data):
		 self._target.start(etree.PI, {})
		 self._target.data(target + " " + data)
		 self._target.end(etree.PI)

def indent(elem, level=0):
	""" Simple indentation for the to-be-written XML.
	
	Taken from http://effbot.org/zone/element-lib.htm#prettyprint
	"""
	
	i = "\n" + level*"  "
	if len(elem):
		if not elem.text or not elem.text.strip():
			elem.text = i + "  "
		if not elem.tail or not elem.tail.strip():
			elem.tail = i
		for elem in elem:
			indent(elem, level+1)
		if not elem.tail or not elem.tail.strip():
			elem.tail = i
	else:
		if level and (not elem.tail or not elem.tail.strip()):
			elem.tail = i
