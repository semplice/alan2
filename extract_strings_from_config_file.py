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

import ConfigParser as cp

cfg = cp.SafeConfigParser()
cfg.read("./alan.conf")

potfile = open("lang/alan2/alan2.pot", "a")
potfile.write("\n")

for sect in cfg.sections():
	for opt in cfg.options(sect):
		# *label*
		if "label" in opt:
			# Yay!
			potfile.write("""# alan.conf
msgid "%s"
msgstr ""

""" % cfg.get(sect, opt))

potfile.close()
