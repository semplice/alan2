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

namespaces = {"ob":"http://openbox.org/3.5/rc"}
etree.register_namespace('',namespaces["ob"])

OPENBOX_CONFIGURATION_DIR = os.path.expanduser("~/.config/openbox")
DEFAULT_PATH=os.path.expanduser("~/.config/alan-menus")

# Create and parse arguments
parser = argparse.ArgumentParser(description="Modifies Openbox configuration to enable/disable alan2 modules.")
parser.add_argument(
	"extension",
	nargs="?",
	help="the extension to process",
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

args = parser.parse_args()
if not args.list and not args.extension:
	raise Exception("You must specify an extension!")

## Welcome to alan2!

# Open alan2 configuration
configuration = config.Configuration(args.extension)
map_as_main = configuration.settings["alan"]["map_as_main"]

# Open openbox configuration
tree = etree.parse(os.path.join(OPENBOX_CONFIGURATION_DIR, "rc.xml"), tree_helpers.PIParser())
document = tree.getroot()
root = document.find("ob:openbox_config", namespaces=namespaces)
menu = root.find("ob:menu", namespaces=namespaces)

# Get and parse all enabled modules...
ENABLED_MODULES = {}
for child in menu.findall("ob:file", namespaces=namespaces):
	if os.path.dirname(child.text) == DEFAULT_PATH:
		# it's ours!
		ENABLED_MODULES[".".join(os.path.basename(child.text).split(".")[:-1])] = child

# What should we do?
if args.list:
	# Should do a list!
	for module, child in ENABLED_MODULES.items():
		print("Extension '%s', cached menu file at %s." % (module, child.text))
	
	sys.exit()
elif args.enable:
	# Should enable a module!
	if args.extension in ENABLED_MODULES:
		# Already enabled!
		raise Exception("Extension %s already enabled!" % args.extension)
	
	ext = etree.SubElement(menu, "file")
	ext.text = os.path.join(DEFAULT_PATH, "%s.xml" % args.extension)
elif args.disable:
	# Should remove a module!
	if not args.extension in ENABLED_MODULES:
		# Not found :(
		raise Exception("Extension %s is not currently enabled!" % args.extension)
	elif args.extension == map_as_main:
		# Removing the main module would be a kind of pointless...
		raise Exception("Extension %s is currently mapped as the main extension in alan2. Please change alan2's main module in order to disable this." % args.extension)
	
	menu.remove(ENABLED_MODULES[args.extension])
	del ENABLED_MODULES[args.extension]

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
