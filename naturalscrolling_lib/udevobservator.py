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

import pyudev
from pyudev.glib import GUDevMonitorObserver
from naturalscrolling.xinputwarper import XinputWarper
from naturalscrolling_lib.gconfsettings import GConfSettings


class UDevObservator(object):

    def __init__(self):
        self.__observator = None

    def start(self):
        """ Observe added and removed events """
        monitor = pyudev.Monitor.from_netlink(pyudev.Context())
        monitor.filter_by(subsystem="input")
        observer = GUDevMonitorObserver(monitor)
        observer.connect("device-added", self.on_device_added)
        observer.connect("device-removed", self.on_device_removed)
        monitor.enable_receiving()

    def on_update_execute(self, callback):
        """ Define the observator of add and change signals """
        self.__observator = callback

    def gather_devices_names(self):
        """ Gather and return all devices names """
        devices_names = []
        for device in pyudev.Context().list_devices(subsystem="input",
                                                    ID_INPUT_MOUSE=True):
            if device.sys_name.startswith("event"):
                # [1:-1] means remove double quotes
                # at the begining and at the end
                devices_names.append(device.parent["NAME"][1:-1])
        return devices_names

    def gather_devices(self):
        """ Gather and return all devices (name and XID) """
        devices = []
        for device_name in self.gather_devices_names():
            devices.append(
                {XinputWarper().find_xid_by_name(device_name): device_name})
        return devices

    # ~~~~ Callback methods ~~~~
    def on_device_added(self, observer, device):
        """
        Fired method when a new device is added to udev
            - Create key in GConf for this new device
            - Call back observators
        """
        if device.sys_name.startswith("event"):
            XinputWarper().reset_cache()
            print device.sys_name
            GConfSettings().key(XinputWarper().find_xid_by_name(
                device.parent["NAME"][1:-1]), bool).find_or_create()

        self.__observator(self.gather_devices_names())

    def on_device_removed(self, observer, device):
        """
        Fired method when a device is removed from udev
            - Delete key from GConf of the device
            - Call back observators
        """
        if device.sys_name.startswith("event"):
            print device.sys_name
            print device.parent["NAME"]
            xid = XinputWarper().find_xid_by_name(device.parent["NAME"][1:-1])
            print "xid: %s" % xid
            GConfSettings().key(xid).remove()
            XinputWarper().reset_cache()

        self.__observator(self.gather_devices_names())
