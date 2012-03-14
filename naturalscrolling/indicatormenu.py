# -*- coding: utf-8 -*-
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

import os
import gtk
import webbrowser
from naturalscrolling_lib.naturalscrollingconfig import *
from naturalscrolling_lib.gconfsettings import GConfSettings
from naturalscrolling.xinputwarper import XinputWarper


class IndicatorMenu(gtk.Menu):

    def __init__(self):
        gtk.Menu.__init__(self)

        # "Natural Scrolling" item is now dynamic.
        # Look at refresh() method
        self.__natural_scrolling = None

        self.append(self.new_separator())

        menu_sub = gtk.Menu()
        start_at_login = gtk.CheckMenuItem("Start at login")
        if os.path.isfile(get_auto_start_file_path()):
            start_at_login.set_active(True)
        start_at_login.connect("activate", self.on_start_at_login_clicked)
        menu_sub.append(start_at_login)
        start_at_login.show()

        preferences = gtk.MenuItem("Preferences")
        preferences.set_submenu(menu_sub)
        self.append(preferences)
        preferences.show()

        about = gtk.MenuItem("About")
        about.connect("activate", self.on_about_clicked)
        self.append(about)
        about.show()

        self.append(self.new_separator())

        quit = gtk.MenuItem("Quit Natural Scrolling")
        quit.connect("activate", self.on_quit_clicked)
        self.append(quit)
        quit.show()

        self.sync_checked_items_from_gconf()

        self.show()

    def new_separator(self):
        seperator = gtk.SeparatorMenuItem()
        seperator.show()
        return seperator

    def sync_checked_items_from_gconf(self):
        """
        Check all gtk.CheckMenuItem depending on GConf keys values
        """
        for xid in GConfSettings().activated_devices_xids():
            self.update_check_menu_item(xid, True)

    def refresh(self, devices):
        """
        Fire this method with the list of devices to display in order to
        refresh the menu.
        If there is only one device, the "Natural scrolling" menu item will be
        a gtk.CheckMenuItem, but if there are more than one devcice, then
        "Natural scrolling" menu item will be a gtk.Menu of gtk.CheckMenuItem
        per device.
        """
        if self.__natural_scrolling:
            self.remove(self.__natural_scrolling)
            self.__natural_scrolling = None

        if len(devices) == 1:
            self.__natural_scrolling = gtk.CheckMenuItem("Natural Scrolling")
            self.__natural_scrolling.set_tooltip_text(devices[0].keys()[0])
            self.__natural_scrolling.connect("toggled",
                self.on_natural_scrolling_toggled)
            self.__natural_scrolling.show()
        else:
            self.__natural_scrolling = gtk.MenuItem("Natural Scrolling")
            self.__natural_scrolling.show()
            devices_menu = gtk.Menu()
            for device in devices:
                sub_item = gtk.CheckMenuItem(device.values()[0])
                sub_item.set_tooltip_text(device.keys()[0])
                devices_menu.append(sub_item)
                sub_item.connect("toggled", self.on_natural_scrolling_toggled)
                sub_item.show()

            self.__natural_scrolling.set_submenu(devices_menu)

        self.insert(self.__natural_scrolling, 0)

        self.sync_checked_items_from_gconf()

    def on_quit_clicked(self, widget):
        gtk.main_quit()

    def on_natural_scrolling_toggled(self, widget, data=None):
        """
        Fired method when user click on gtk.CheckMenuItem 'Natural Scrolling'
        """
        enabled = widget.get_active()
        natural_scrolling_or_device_name = widget.get_label()

        # When there is only one detected device
        # the label of the gtk.CheckMenuItem is "Natural Scrolling"
        if natural_scrolling_or_device_name == "Natural Scrolling":
            # So the device XID is the id of the first device
            device_xid = XinputWarper().first_xid()
        else:
            device_xid = XinputWarper().find_xid_by_name(widget.get_label())

        GConfSettings().key(device_xid).set_value(enabled)

    def update_check_menu_item(self, xid, enabled):
        """
        Retreive the gtk.CheckMenuItem with the text and set the value
        """
        if not self.__natural_scrolling:
            return

        submenu = self.__natural_scrolling.get_submenu()
        if submenu:
            for widget in self.__natural_scrolling.get_submenu():
                if widget.get_tooltip_text() == xid:
                    widget.set_active(enabled)
        else:
            self.__natural_scrolling.set_active(enabled)

    def on_start_at_login_clicked(self, widget, data=None):
        """
        Fired method when user click on gtk.CheckMenuItem 'Start at login'
        """
        if not os.path.exists(get_auto_start_path()):
            os.makedirs(get_auto_start_path())

        auto_start_file_exists = os.path.isfile(get_auto_start_file_path())
        if widget.get_active():
            if not auto_start_file_exists:
                source = open(get_auto_start_from_data_file_path(), "r")
                destination = open(get_auto_start_file_path(), "w")
                destination.write(source.read())
                destination.close() and source.close()
        else:
            if auto_start_file_exists:
                os.remove(get_auto_start_file_path())

    def click_website(self, dialog, link):
        webbrowser.open(link)

    def on_about_clicked(self, widget, data=None):
        gtk.about_dialog_set_url_hook(self.click_website)

        app_name = "Natural Scrolling"
        about = gtk.AboutDialog()
        about.set_name(app_name)
        about.set_version(appliation_version())
        about.set_icon(
            gtk.gdk.pixbuf_new_from_file(get_data_path() +
                                         "/media/naturalscrolling.svg"))
        about.set_logo(
            gtk.gdk.pixbuf_new_from_file(get_data_path() +
                                         "/media/naturalscrolling.svg"))
        about.set_website(appliation_website())
        about.set_website_label("%s Website" % app_name)
        about.set_authors(["Charalampos Emmanouilidis <ce@eumorphed.com>",
                           "Guillaume Hain <zedtux@zedroot.org>"])
        about.set_copyright("Copyright © 2011 Eumorphed UG")
        about.set_wrap_license(True)
        about.set_license(("%s is free software; you can redistribute it "
            "and/or modify it under the terms of the GNU General "
            "Public License as published by the Free Software Foundation; "
            "either version 3 of the License, or (at your option) any later "
            "version.\n\n%s is distributed in the hope that it will be "
            "useful, but WITHOUT ANY WARRANTY; without even the implied "
            "warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE."
            "  See the GNU General Public License for more details.\n\n"
            "You should have received a copy of the GNU General Public "
            "License along with %s; if not, write to the Free Software "
            "Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, "
            "MA 02110-1301, USA") % (app_name, app_name, app_name))
        about.run()
        about.destroy()
