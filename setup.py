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

from distutils.core import setup

setup(
	name='alan2',
	version='1.20.2',
	description='Openbox Menu Extension Framework and Builder',
	author='Eugenio Paolantonio',
	author_email='me@medesimo.eu',
	url='https://github.com/semplice/alan2',
	scripts=['alan-config.py', 'alan-menu-updater.py', 'alan-pipe.py', 'reference-watcher.py'],
	packages=['alan', 'alan.core', 'alan.core.objects', 'alan.extensions'],
	data_files=[
		("/usr/share/alan2", ["alan2-setup.sh"]),
		("/etc/xdg/autostart", ["alan-reference-watcher.desktop"]),
		("/etc/alan", ["alan.conf", "alan-vera.conf", "semplice-vera.distrib", "semplice.distrib"]),
		(
			"/etc/alan/watchers",
			[
				"watchers/xdgmenu.watcher",
				"watchers/places.watcher",
				"watchers/logout.watcher",
				"watchers/appearance.watcher",
				"watchers/main.watcher",
			]
		)
	
	],
	requires=['ConfigParser', 'commands', 'gettext', 'gmenu', 'locale', 'os', 'sys', 're', 'shutil', 'xml.etree.ElementTree', 'quickstart.translations', 'gtk', 'nala'],
)
