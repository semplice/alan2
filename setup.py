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

import os

from distutils.core import setup, Command
from distutils.command.build import build
from distutils.command.install import install

import subprocess
import shutil

import ConfigParser as cp

l10n_path = "./lang"

APP_NAME = "alan2"
CONFIG_FILES = ["./alan.conf", "./alan-vera.conf"]

class CreatePotTemplate(Command):
	"""
	Creates a .pot template.
	"""
	
	description = "creates a .pot localization template from the program sources."
	user_options = []
	
	def initialize_options(self):
		"""
		Initialize options
		"""
		
		self.cwd = None
	
	def finalize_options(self):
		"""
		Finalize options
		"""
		
		self.cwd = os.getcwd()
	
	def run(self):
		"""
		Does things.
		"""
		
		assert os.getcwd() == self.cwd, "You must be in the package root: %s" % self.cwd
		
		py_files = []
		
		for directory, dirnames, filenames in os.walk("."):
			for file_ in filenames:
				if file_.endswith(".py"):
					py_files.append(os.path.join(directory, file_))
					
		subprocess.call([
			"xgettext",
			"--language=Python",
			"--from-code=utf-8",
			"--keyword=_",
			"--output=%s" % os.path.join(self.cwd, l10n_path, APP_NAME, "%s.pot" % APP_NAME),
		] + py_files)

		for conf in CONFIG_FILES:
			cfg = cp.SafeConfigParser()
			cfg.read(conf)
			
			with open("lang/alan2/alan2.pot", "a+") as potfile:
				potfile.write("\n\n")

				lines = potfile.readlines()

				# Fake ugly counter
				counter = 0

				for sect in cfg.sections():
					for opt in cfg.options(sect):
						# *label*
						if "label" in opt and not ("msgid \"%s\"\n" % cfg.get(sect, opt)) in lines:
							# Yay!
							counter += 1
							potfile.write("""
#: %s:%i
msgid "%s"
msgstr ""
""" % (os.path.basename(conf), counter, cfg.get(sect, opt)))
		

class CustomBuild(build):
	"""
	Hooks.
	"""
	
	def run(self):
		"""
		Runs the installation.
		"""
		
		build.run(self)
		
		# Build mos
		for directory, dirnames, filenames in os.walk(l10n_path):
			for file_ in filenames:
				if file_.endswith(".po"):
					source = os.path.join(directory, file_)
					target_dir = os.path.join("./build", directory)
					target = os.path.join(target_dir, file_.replace(".po",".mo"))
					
					if not os.path.exists(target_dir):
						os.makedirs(target_dir)
					
					print("Compiling translation %s" % file_)
					subprocess.call(["msgfmt", "--output-file=%s" % target, source])

class CustomInstall(install):
	"""
	Hooks.
	"""
	
	def run(self):
		"""
		Runs the installation.
		"""
		
		install.run(self)
		
		# Install mos
		for directory, dirnames, filenames in os.walk(os.path.join("./build", l10n_path)):
			for file_ in filenames:
				if file_.endswith(".mo"):
					source = os.path.join(directory, file_)
					target_dir = os.path.join(
						self.root if self.root else "/",
						"usr/share/locale",
						file_.replace(".mo",""),
						"LC_MESSAGES"
					)
					target = os.path.join(target_dir, os.path.basename(directory) + ".mo")
					
					if not os.path.exists(target_dir):
						os.makedirs(target_dir)
					
					shutil.copyfile(source, target)
					os.chmod(target, 644)

setup(
	cmdclass={
		"pot": CreatePotTemplate,
		"build": CustomBuild,
		"install": CustomInstall
	},
	name=APP_NAME,
	version='1.30.2',
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
				#"watchers/logout.watcher",
				"watchers/logout_vera.watcher",
				"watchers/appearance.watcher",
				"watchers/main.watcher",
			]
		)
	
	],
	requires=['ConfigParser', 'commands', 'gettext', 'gmenu', 'locale', 'os', 'sys', 're', 'shutil', 'xml.etree.ElementTree', 'quickstart.translations', 'gi.repository.Gtk', 'nala'],
)
