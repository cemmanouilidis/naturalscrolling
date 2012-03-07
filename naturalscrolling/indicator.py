### BEGIN LICENSE
# Copyright (C) 2011 Guillaume Hain <zedtux@zedroot.org>
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>
### END LICENSE

import gtk
import appindicator

from naturalscrolling_lib import naturalscrollingconfig
from naturalscrolling_lib.gconfsettings import GConfSettings
from naturalscrolling_lib.udevobservator import UDevObservator
from naturalscrolling.indicatormenu import IndicatorMenu


class Indicator(object):
    # Singleton
    _instance = None
    _init_done = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Indicator, cls).__new__(cls, *args,
                                                          **kwargs)
        return cls._instance

    def __init__(self):
        # Initialize a new AppIndicator
        self.indicator = appindicator.Indicator(
            "natural-scrolling-indicator",
            "natural-scrolling-status-not-activated",
            appindicator.CATEGORY_APPLICATION_STATUS)
        media_path = "%s/media/" % naturalscrollingconfig.get_data_path()
        self.indicator.set_icon_theme_path(media_path)
        self.indicator.set_attention_icon(
            "natural-scrolling-status-activated")

        menu = IndicatorMenu()
        self.indicator.set_menu(menu)

        # Initialize the UDev client
        udev_observator = UDevObservator()
        udev_observator.on_update_execute(menu.refresh)
        udev_observator.start()

        # Force the first refresh of the menu in order to populate it.
        menu.refresh(udev_observator.gather_devices_names_with_xid())

        GConfSettings().initialize(udev_observator.gather_devices())

    def status_attention(self):
        self.set_status(appindicator.STATUS_ATTENTION)

    def status_active(self):
        self.set_status(appindicator.STATUS_ACTIVE)

    def isreversed(self):
        return True

    def check_scrolling(self):
        if self.isreversed():
            self.indicator.set_status(appindicator.STATUS_ATTENTION)
        else:
            self.indicator.set_status(appindicator.STATUS_ACTIVE)
        return True

    def start(self):
        self.check_scrolling()
        try:
            gtk.main()
        except KeyboardInterrupt:
            pass
