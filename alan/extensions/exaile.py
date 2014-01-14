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

class Exaile:
	def playpause(self, iface):
		iface.PlayPause()

	def stop(self, iface):
		iface.Stop()

	def prev(self, iface):
		iface.Prev()

	def next(self, iface):
		iface.Next()

class Extension(extension.Extension):
	
	extensionName = "exaile"
	
	def generate(self):

		self.add(Header("Exaile"))
					
		try:
			self.remote_object = bus.get_object("org.exaile.Exaile","/org/exaile/Exaile")
			self.iface = dbus.Interface(self.remote_object, "org.exaile.Exaile")

			if self.iface.GetState() == "playing":
				self.add(self.return_executable_item(_("Pause"), "alan-show-extension %s playpause" % sys.argv[1], icon="media-playback-pause"))
			else:
				self.add(self.return_executable_item(_("Play"), "alan-show-extension %s playpause" % sys.argv[1], icon="media-playback-start"))
				
			self.add(self.return_executable_item(_("Stop"), "alan-show-extension %s stop" % sys.argv[1], icon="media-playback-stop"))
	
			self.add(Separator())
	
			self.add(self.return_executable_item(_("Previous"), "alan-show-extension %s prev" % sys.argv[1], icon="media-skip-backward"))
			self.add(self.return_executable_item(_("Next"), "alan-show-extension %s next" % sys.argv[1], icon="media-skip-forward"))
			
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

if len(sys.argv) > 2:
	try:
		remote_object = bus.get_object("org.exaile.Exaile","/org/exaile/Exaile")
		iface = dbus.Interface(remote_object, "org.exaile.Exaile")
		if sys.argv[2] == "playpause":
			Exaile().playpause(iface)
		elif sys.argv[2] == "stop":
			Exaile().stop(iface)
		elif sys.argv[2] == "prev":
			Exaile().prev(iface)
		elif sys.argv[2] == "next":
			Exaile().next(iface)
	except:
		pass
