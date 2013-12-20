#!/bin/bash
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
# This script setups alan2 (useful to distributors only).

LIST_DIRECTORY="/etc/alan"

case "$1" in
	"")
		echo "Please specify the module list. See -h for more details." >&2
		exit 1
		;;
	"-h"|"--help")
		cat <<EOF
$0 - wrapper to alan-config to bulk enable alan2 modules.
USAGE: $0 <list>

'list' should not contain paths and file extension.
The search path is $LIST_DIRECTORY.

Example:
 $0 semplice
	
 Enables the modules specified in $LIST_DIRECTORY/semplice.distrib.

This script is not really useful for the end-user.
If you are an end-user, simply use /usr/bin/alan-config.
EOF
		exit 0
		;;
esac

LIST="$LIST_DIRECTORY/$1.distrib"

if [ ! -e "$LIST" ]; then
	# Whoops... file doesn't exist...
	echo "$LIST not found. Aborting." >&2
	exit 1
fi

modules="`xargs -a $LIST`"

for module in $modules; do
	alan-menu-updater $module
done

exec alan-config --setup "$modules"
