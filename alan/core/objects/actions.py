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
# This file contains openbox actions.

from alan.core.objects.baseobject import BaseObject, DynamicObject

class BaseAction(BaseObject):
	""" A BaseAction object. Extension creators should not need this. """
	
	objectName = "action"
	actionName = None
	
	def __init__(self):
		""" Initializes the object. """
		
		BaseObject.__init__(self)
		if self.actionName:
			self.set("name", self.actionName)

class ExecuteAction(BaseAction):
	""" An Action which executes applications. """
	
	actionName = "Execute"
	
	def __init__(self, command, prompt=None):
		""" Initializes the object.
		
		'command' is the command to execute.
		'prompt', if not None, contains the string to show in a Yes/No
		popup dialog. If None, the popup will not be displayed. """
		
		BaseAction.__init__(self)
		
		self.append(DynamicObject("command", command))
		if prompt:
			self.append(DynamicObject("prompt", prompt))
		
		
