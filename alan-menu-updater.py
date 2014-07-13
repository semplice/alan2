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
#    Eugenio "g7" Paolantonio <me@medesimo.eu>
#

import quickstart.translations

tr = quickstart.translations.Translation("alan2")
tr.install()

import alan.core.main as main
import alan.core.config as config

import argparse
import os

# Create and parse arguments
parser = argparse.ArgumentParser()
parser.add_argument(
	"extension",
	help="the extension to process"
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

parser.add_argument(
	"-t", "--target",
	help="the target file. Defaults to ~/.config/alan-menus/<extension>.xml"
)

args = parser.parse_args()

## Welcome to alan2!
DIRECTORY = os.path.expanduser(args.directory)

DEFAULT_PATH=os.path.join(DIRECTORY, "alan-menus")
# Generate directory if it doesn't exist
if not os.path.exists(DEFAULT_PATH):
	os.makedirs(DEFAULT_PATH)

# If target is not specified, use our default
if not args.target:
	args.target = os.path.join(DEFAULT_PATH, "%s.xml" % args.extension)

# Get extension configuration
configuration = config.Configuration(args.extension, DIRECTORY, args.profile)

# Import extension
extension_module = main.import_extension(args.extension)

# Get extension object
extension = extension_module.Extension(configuration=configuration)

# Generate menu
extension.generate()

# Write menu
extension.write_menu(args.target)
