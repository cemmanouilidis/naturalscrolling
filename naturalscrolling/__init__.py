# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (C) 2011 Eumorphed UG,
# Charalampos Emmanouilidis <ce@eumorphed.com>
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

import optparse

from naturalscrolling_lib.naturalscrollingconfig import *
from naturalscrolling.indicator import Indicator
from naturalscrolling_lib.gconfsettings import GConfSettings
from naturalscrolling.xinputwarper import XinputWarper


def main():
    """Support for command line options"""
    parser = optparse.OptionParser(version="%%prog %s" % appliation_version())
    parser.add_option("-v", "--verbose", action="count", dest="verbose",
        help="Show debug messages (-vv debugs naturalscrolling_lib also)")
    (options, args) = parser.parse_args()

    # Initialize the GConf client
    GConfSettings().server().on_update_fire(
        XinputWarper().enable_natural_scrolling)

    Indicator().start()
