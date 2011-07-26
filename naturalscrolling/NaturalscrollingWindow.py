# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import gettext
from gettext import gettext as _
gettext.textdomain('naturalscrolling')

import gtk
import logging
logger = logging.getLogger('naturalscrolling')

from naturalscrolling_lib import Window
from naturalscrolling.AboutNaturalscrollingDialog import AboutNaturalscrollingDialog
from naturalscrolling.PreferencesNaturalscrollingDialog import PreferencesNaturalscrollingDialog

# See naturalscrolling_lib.Window.py for more details about how this class works
class NaturalscrollingWindow(Window):
    __gtype_name__ = "NaturalscrollingWindow"
    
    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the main window"""
        super(NaturalscrollingWindow, self).finish_initializing(builder)

        self.AboutDialog = AboutNaturalscrollingDialog
        self.PreferencesDialog = PreferencesNaturalscrollingDialog

        # Code for other initialization actions should be added here.

