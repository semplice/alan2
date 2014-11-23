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
#	Eugenio "g7" Paolantonio <me@medesimo.eu>
#
# This file contains the mpris extension.

import alan.core.extension as extension
from alan.core.objects.separator import Header, Separator
from alan.core.objects.item import Item
from alan.core.objects.actions import ExecuteAction

import sys
import dbus

# Why are we using dbus here instead of Gio? Because every millisecond
# counts.

# Initialize the session bus
bus = dbus.SessionBus()

class InterfaceWithProperties(dbus.Interface):
	"""
	A dbus.Interface variant that provides an easy access to interface
	properties via the standard DBus org.freedesktop.DBus.Properties
	interface.
	"""
	
	def __init__(self, obj, iface_name, properties_iface=None):
		"""
		Initializes the object.
		The usage is the same as dbus_interface, with an optional
		properties_iface keyword.
		
		If None, the DBus properties interface will be get from the given
		object (obj).
		If False, the Interface will behave like a normal dbus.Interface
		instance.
		Otherwise, the given interface will be used to access the
		properties.
		"""
		
		dbus.Interface.__init__(self, obj, iface_name)
		
		self._properties = []
		self.iface_name = iface_name
		
		if properties_iface == None:
			properties_iface = dbus.Interface(
				obj,
				"org.freedesktop.DBus.Properties"
			)
		
		if properties_iface:
			self._properties = properties_iface.GetAll(iface_name).keys()
			
		self.properties_iface = properties_iface
		
	def __getattr__(self, key):
		"""
		Overrides __getattr__ so that we can check for properties.
		"""
		
		if key in self._properties:	
			return self.properties_iface.Get(self.iface_name, key)
		else:
			return dbus.Interface.__getattr__(self, key)

class Extension(extension.Extension):
	"""
	This extension manages every media player application
	that uses the MPRIS specification.
	"""
	
	extensionName = "mpris"
	
	@property
	def players(self):
		"""
		Returns a list of active media players.
		"""
		
		iface = dbus.Interface(
			bus.get_object("org.freedesktop.DBus", "/"),
			"org.freedesktop.DBus"
		)
		
		players = []
		for name in iface.ListNames():
			if name.startswith("org.mpris.MediaPlayer2."):
				players.append(name)
		
		if not len(players):
			# Add fake player
			players.append(None)
		
		return players
	
	def get_player_interfaces(self, name, ifaces=(None, "Player")):
		"""
		Returns the player's DBus interfaces.
		"""
		
		result = []
		
		obj = bus.get_object(name, "/org/mpris/MediaPlayer2")
		
		for iface in ifaces:
			result.append(
				InterfaceWithProperties(
					obj,
					"org.mpris.MediaPlayer2" if not iface else "org.mpris.MediaPlayer2.%s" % iface
				)
			)
		
		return result
	
	def handle_arguments(self):
		"""
		Handles arguments
		"""
		
		if len(self.arguments) != 2:
			# We require two arguments (player and action)
			raise Exception("Two arguments required! (player and action)")
		
		player, action = self.arguments
		
		if action not in ("PlayPause", "Stop", "Previous", "Next", "Raise"):
			# Action not allowed
			raise Exception("Action %s not allowed" % action)
		
		app_iface, player_iface = self.get_player_interfaces(player)
		
		if action in ("Raise"):
			# app_iface
			iface = app_iface
		else:
			iface = player_iface
		
		return getattr(iface, action)()
	
	def generate(self):
		"""
		Generates the menu.
		"""
		
		if self.arguments:
			return self.handle_arguments()
		
		for player in self.players:
			
			if player == None:
				self.add(Header(_("Music")))
				self.add(self.return_executable_item(_("No music player running"), None, None, icon="preferences-desktop-sound"))
				break
			
			# Get interfaces
			app_iface, player_iface = self.get_player_interfaces(player)
			
			# Header
			self.add(Header(app_iface.Identity))
						
			status = player_iface.PlaybackStatus
			
			if status != "Stopped":
				if player_iface.CanPause and status == "Playing":
					self.add(self.return_executable_item(_("Pause"), player, "PlayPause", icon="media-playback-pause"))
				
				if player_iface.CanPlay and status == "Paused":
					self.add(self.return_executable_item(_("Play"), player, "PlayPause", icon="media-playback-start"))
				
				if player_iface.CanStop:
					self.add(self.return_executable_item(_("Stop"), player, "Stop", icon="media-playback-stop"))
				
				self.add(Separator())
				
				if player_iface.CanGoPrevious:
					self.add(self.return_executable_item(_("Previous"), player, "Previous", icon="media-skip-backward"))
				
				if player_iface.CanGoNext:
					self.add(self.return_executable_item(_("Next"), player, "Next", icon="media-skip-forward"))
				
				# Track informations
				metadata = player_iface.Metadata
				try:
					self.add(Separator())
					self.add(self.return_executable_item(str(metadata["xesam:title"].replace("_","__")), None, None, icon="audio-x-generic"))
					self.add(self.return_executable_item(str(metadata["xesam:album"].replace("_","__")), None, None, icon="media-optical"))
					self.add(self.return_executable_item(str(metadata["xesam:artist"][0].replace("_","__")), None, None, icon="audio-input-microphone"))
				except:
					# No one cares
					pass
			else:
				self.add(self.return_executable_item(_("%s is not playing.") % app_iface.Identity, player, "Raise", icon=None))
			
	
	def return_executable_item(self, label, player, player_action, icon=None):
		""" Returns an executable item. """
				
		item = Item(label=label, icon=self.IconPool.get_icon(icon))
		if player and player_action:
			action = ExecuteAction("alan-pipe %s -a \"%s %s\"" % (self.extensionName, player, player_action))
			item.append(action)
		
		return item
