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
#	Luca B. <sidtux _AT_ gmail _DOT_ com>
#	Eugenio "g7" Paolantonio <me@medesimo.eu>
#
# This file contains the exaile extension.

import alan.core.extension as extension
from alan.core.objects.separator import Header, Separator
from alan.core.objects.item import Item
from alan.core.objects.menu import Menu
from alan.core.objects.actions import ExecuteAction

import os, sys, dbus

executable = " ".join(sys.argv)

# Initialize the session bus
bus = dbus.SessionBus()

class Extension(extension.Extension):
	
	extensionName = "exaile"
	
	def generate(self):

		if self.arguments:
			arg = self.arguments[0]
			try:
				remote_object = bus.get_object("org.exaile.Exaile","/org/exaile/Exaile")
				iface = dbus.Interface(remote_object, "org.exaile.Exaile")
				if arg == "playpause":
					iface.PlayPause()
				elif arg == "stop":
					iface.Stop()
				elif arg == "prev":
					iface.Prev()
				elif arg == "next":
					iface.Next()
			except:
				pass
			
			return

		self.add(Header("Exaile"))
					
		try:
			self.remote_object = bus.get_object("org.exaile.Exaile","/org/exaile/Exaile")
			self.iface = dbus.Interface(self.remote_object, "org.exaile.Exaile")

			if self.iface.GetState() == "playing":
				self.add(self.return_executable_item(_("Pause"), "alan-pipe %s -a playpause" % sys.argv[1], icon="media-playback-pause"))
			else:
				self.add(self.return_executable_item(_("Play"), "alan-pipe %s -a playpause" % sys.argv[1], icon="media-playback-start"))
				
			self.add(self.return_executable_item(_("Stop"), "alan-pipe %s -a stop" % sys.argv[1], icon="media-playback-stop"))
	
			self.add(Separator())
	
			self.add(self.return_executable_item(_("Previous"), "alan-pipe %s -a prev" % sys.argv[1], icon="media-skip-backward"))
			self.add(self.return_executable_item(_("Next"), "alan-pipe %s -a next" % sys.argv[1], icon="media-skip-forward"))
			
			self.add(Separator())
			# Displays infos about the current song
			if(self.iface.IsPlaying()):
				self.add(self.return_executable_item(self.iface.GetTrackAttr("title"), "echo", icon="audio-x-generic"))
				self.add(self.return_executable_item(self.iface.GetTrackAttr("album"), "echo", icon="media-optical"))
				self.add(self.return_executable_item(self.iface.GetTrackAttr("artist"), "echo", icon="audio-input-microphone"))
			else:
				self.add(self.return_executable_item(_("Exaile is not playing."), "echo", icon=""))
		except dbus.exceptions.DBusException:
			self.add(self.return_executable_item(_("Open Exaile"), "exaile", icon="exaile"))

	def return_executable_item(self, label, target, icon=None):
		""" Returns an executable item. """
				
		item = Item(label=label, icon=self.IconPool.get_icon(icon))
		action = ExecuteAction(target)
		item.append(action)
		
		return item
