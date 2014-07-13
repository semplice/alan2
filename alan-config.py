#!/usr/bin/env python
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
#	 Eugenio "g7" Paolantonio <me@medesimo.eu>
#

import xml.etree.ElementTree as etree

import alan.core.tree_helpers as tree_helpers
import alan.core.config as config

import argparse
import os
import sys

# Create and parse arguments
parser = argparse.ArgumentParser(description="Modifies Openbox configuration to enable/disable alan2 modules.")
parser.add_argument(
	"extension",
	nargs="?",
	help="the extension to process",
)

parser.add_argument(
	"-i", "--directory",
	help="directory where to look for configuration files (default: ~/.config)",
	default="~/.config"
)

parser.add_argument(
	"-p", "--profile",
	help="the profile to use"
)

group = parser.add_mutually_exclusive_group()
group.add_argument(
	"-e", "--enable",
	help="enable the extension",
	action="store_true"
)

group.add_argument(
	"-d", "--disable",
	help="disable the extension",
	action="store_true"
)

group.add_argument(
	"-l", "--list",
	help="list active estensions",
	action="store_true"
)

group.add_argument(
	"-s", "--setup",
	help="setups alan2",
	action="store_true"
)

args = parser.parse_args()
if not (args.list or args.setup) and not args.extension:
	raise Exception("You must specify an extension!")

## Welcome to alan2!
DIRECTORY = os.path.expanduser(args.directory)

OPENBOX_CONFIGURATION_DIR = os.path.join(DIRECTORY, "openbox")
DEFAULT_PATH=os.path.join(DIRECTORY, "alan-menus")

# Open alan2 configuration
configuration = config.Configuration(args.extension, DIRECTORY, args.profile)
map_as_main = configuration.settings["alan"]["map_as_main"]

if args.extension:
	args.extension = args.extension.split(" ")
	# Check for map_as_main
	if map_as_main in args.extension:
		# Found it, ensure we put it at the end
		if args.extension.index(map_as_main) != len(args.extension)-1:
			# It isn't at the end, remove it and reappend again
			args.extension.remove(map_as_main)
			args.extension.append(map_as_main)

# Open openbox configuration
tree = etree.parse(os.path.join(OPENBOX_CONFIGURATION_DIR, "rc.xml"), tree_helpers.PIParser())
document = tree.getroot()
root = document.find("ob:openbox_config", namespaces={"ob":"http://openbox.org/3.5/rc"})
if root is None:
	# openbox-3.4
	root = document.find("ob3:openbox_config", namespaces={"ob3":"http://openbox.org/3.4/rc"})
	namespaces = {"ob":"http://openbox.org/3.4/rc"}
else:
	namespaces = {"ob":"http://openbox.org/3.5/rc"}
etree.register_namespace('',namespaces["ob"])

menu = root.find("ob:menu", namespaces=namespaces)

# Get and parse all enabled modules...
ENABLED_MODULES = {}
_openbox_menu = []
for child in menu.findall("ob:file", namespaces=namespaces):
	if os.path.dirname(child.text) == DEFAULT_PATH:
		# it's ours!
		ENABLED_MODULES[".".join(os.path.basename(child.text).split(".")[:-1])] = child
	elif child.text in ("menu.xml","menu-static.xml"):
		# Openbox default? Maybe. Cache the child, so that we can use it
		# if we are going to setup alan2.
		_openbox_menu.append(child)

# What should we do?
if args.setup:
	# Setup!
	for _menu in _openbox_menu:
		# Remove found menus, they will clash with alan2 *for sure*.
		menu.remove(_menu)

	# If there are some extensions in the arguments, it's a good thing
	# to set args.enable to True so that we do not need to recall this
	# executable to enable things...
	if args.extension:
		args.enable = True

if args.list:
	# Should do a list!
	for module, child in ENABLED_MODULES.items():
		print("Extension '%s', cached menu file at %s." % (module, child.text))
	
	sys.exit()
elif args.enable:
	# Should enable a module!
	for extension in args.extension:
		if extension in ENABLED_MODULES:
			# Already enabled!
			raise Exception("Extension %s already enabled!" % extension)
		
		ext = etree.SubElement(menu, "file")
		ext.text = os.path.join(DEFAULT_PATH, "%s.xml" % extension)
elif args.disable:
	# Should remove a module!
	for extension in args.extension:
		if not extension in ENABLED_MODULES:
			# Not found :(
			raise Exception("Extension %s is not currently enabled!" % extension)
		elif extension == map_as_main:
			# Removing the main module would be a kind of pointless...
			raise Exception("Extension %s is currently mapped as the main extension in alan2. Please change alan2's main module in order to disable this." % extension)
		
		menu.remove(ENABLED_MODULES[extension])
		del ENABLED_MODULES[extension]

# This is not a great thing to do, but we must: ensure we have the module
# mapped as main at the end of the subsection.
if map_as_main in ENABLED_MODULES:
	# Ok, it's there, and it hasn't be touched (likely it is not the last anymore)
	menu.remove(ENABLED_MODULES[map_as_main])
	menu.append(ENABLED_MODULES[map_as_main])

tree_helpers.indent(root)
tree._setroot(root) # fixme?
tree.write(os.path.join(OPENBOX_CONFIGURATION_DIR, "rc.xml"),
	xml_declaration=True,
	encoding="utf-8",
	method="xml"
)
