# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (C) 2011 Eumorphed UG, Charalampos Emmanouilidis <charalampos.emmanouilidis@eumorphed.com>
# 
# This program is free software: you can redistribute it and/or modify it 
# under the terms of the GNU General Public License version 3, as published 
# by the Free Software Foundation.
# 
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranties of 
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
# PURPOSE.  See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along 
# with this program.  If not, see <http://www.gnu.org/licenses/>.
### END LICENSE

import optparse

import gettext
from gettext import gettext as _
gettext.textdomain('naturalscrolling')

import gtk

from naturalscrolling import NaturalscrollingIndicator

#from naturalscrolling_lib import set_up_logging, preferences, get_version
from naturalscrolling_lib import set_up_logging, get_version

def parse_options():
    """Support for command line options"""
    parser = optparse.OptionParser(version="%%prog %s" % get_version())
    parser.add_option(
        "-v", "--verbose", action="count", dest="verbose",
        help=_("Show debug messages (-vv debugs naturalscrolling_lib also)"))
    (options, args) = parser.parse_args()

    set_up_logging(options)

def main():
    'constructor for your class instances'
    parse_options()

    # preferences
    # set some values for our first session
    # TODO: replace defaults with your own values
    default_preferences = {
    'example_entry': 'I remember stuff',
    }

    #preferences.update(default_preferences)
    # user's stored preferences are used for 2nd and subsequent sessions
    #preferences.db_connect()
    #preferences.load()

    # Run the application.    
    indicator  = NaturalscrollingIndicator.NaturalscrollingIndicator() 
    indicator.main()
    
    #preferences.save()

