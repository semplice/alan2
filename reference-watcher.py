#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# reference-watcher - An example watcher for alan2
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
# This file contains a reference python watcher based on python-nala libraries.
#

import sys, os, time

import subprocess

from gi.repository import GLib

from nala.watchers import WatcherPool
from nala.queue import Queue
from nala.applications import Application

from ConfigParser import SafeConfigParser

DEFAULT_PATH=os.path.expanduser("~/.config/alan-menus")
ALAN2_BUILDER_PATH=os.path.expanduser("/usr/bin/alan-menu-updater")

def add_to_queue(pool, watcher, trigger, event, queue):
	""" Add to queue. """
	
	return queue.add_to_queue(watcher, trigger, event)

def do_something(queue, apps, lst):
	""" Fired when ready to regenerate the menus """

	processes = []

	print "GOT QUEUE!", apps, lst
	# Regenerate!
	for app in apps:
		name = app.path
		processes.append(subprocess.Popen([ALAN2_BUILDER_PATH, name], shell=False))
	
	while processes != []:
		# Poll every active process
		for proc in processes:
			if proc.poll != None:
				# Yeah, remove it
				processes.remove(proc)
		time.sleep(0.1)
	
	# Reconfigure openbox
	subprocess.Popen(["openbox", "--reconfigure"], shell=False)

# Hello all...

# Should setup?
if not os.path.exists(DEFAULT_PATH):
	# Yeah babe!
	ret = subprocess.call(["/usr/share/alan2/alan2-setup.sh", "semplice"]) # FIXME, we don't like hardcoded things
	if ret > 0:
		# :/
		raise Exception("Unable to setup alan2.")
	
	# Reconfigure openbox
	subprocess.Popen(["openbox", "--reconfigure"], shell=False)

# parse the watchers/
applications = []
files = {}
applications_objects = {}

pool = WatcherPool()
queue = Queue(3)

for application in os.listdir("/etc/alan/watchers/"):
	
	_file = os.path.join("/etc/alan/watchers", application)
	application = application.replace(".watcher","")
		
	cfg = SafeConfigParser()
	cfg.read(_file)
		
	applications.append(cfg.get("nala", "application"))
	
	# Get files
	_files = []
	if cfg.has_option("nala", "files"):
		__files = cfg.get("nala", "files").split(" ")
	else:
		__files = []
	__files += ["/etc/alan/alan.conf", os.path.expanduser("~/.gtkrc-2.0")]
	
	for _file in __files:
		path = os.path.expanduser(_file)
		if os.path.islink(path):
			path = os.readlink(path)
		_files.append(path)
	
	files[application] = _files
	
	# Add to pool and queue
	applications_objects[application] = Application(application, files[application])
	pool.add_watcher(applications_objects[application].triggers)
	queue.add_application(applications_objects[application])

pool.connect("watcher-changed", add_to_queue, queue)
queue.connect("processable", do_something)

print files

if __name__ == "__main__":
	loop = GLib.MainLoop()
	loop.run()
