# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (C) 2011 Charalampos Emmanouilidis,
# Charalampos Emmanouilidis <chrys.emmanouilidis@gmail.com>
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>
### END LICENSE

import sys
import argparse
import gettext

from naturalscrolling_lib.naturalscrollingconfig import *
from naturalscrolling.indicator import Indicator
from naturalscrolling_lib.gconfsettings import GConfSettings
from naturalscrolling.xinputwarper import XinputWarper
from naturalscrolling_lib.debugger import Debugger

gettext.install("naturalscrolling", get_locale_path())

def main():
    """Support for command line options"""
    parser = argparse.ArgumentParser(prog="Natural Scrolling", description=_("Natural Scrolling is a GNOME Applet allowing you to reverse the direction of scrolling"), add_help=False)
    parser.add_argument("--version", action="version", version="NaturalScrolling %s" % appliation_version(),
        help=_("Show naturalscrolling's version number and exit"))
    parser.add_argument("--help", "-h", action="help",
        help=_("Show this help message and exit"))
    parser.add_argument("--verbose", "-v", action="count", dest="verbose",
        help=_("Show debug messages (-vv debugs naturalscrolling_lib also)"))
    parser.add_argument("--debug", "-d", action="store_true",
        help=_("Enable debuging"))
    args = parser.parse_args()

    if args.debug:
        Debugger().execute()
        sys.exit(0)

    # Initialize the GConf client
    GConfSettings().server().on_update_fire(
        XinputWarper().enable_natural_scrolling)

    Indicator().start()
