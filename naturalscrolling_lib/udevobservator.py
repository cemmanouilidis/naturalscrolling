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

    def gather_devices_names_with_xid(self):
        """ Gather and return all devices names """
        devices_names = []
        devices = pyudev.Context().list_devices(subsystem="input").__iter__()
        while True:
            try:
                device = devices.next()
                if device.sys_name.startswith("event"):
                    try:
                        device_name = device.parent["NAME"][1:-1]
                        if XinputWarper().find_xid_by_name(device_name):
                            # [1:-1] means remove double quotes
                            # at the begining and at the end
                            devices_names.append(device_name)
                    except KeyError:
                        print ("Warning: The device parent with sys_name %s "
                               "doesn't have a NAME key." % device.sys_name)
            except pyudev.DeviceNotFoundAtPathError:
                # next() raise this exception when we try to open a removed
                # device
                pass
            except StopIteration:
                break

        return devices_names

    def gather_devices(self):
        """ Gather and return all devices (name and XID) """
        devices = []
        for device_name in self.gather_devices_names_with_xid():
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
            GConfSettings().key(XinputWarper().find_xid_by_name(
                device.parent["NAME"][1:-1]), bool).find_or_create()

        self.__observator(self.gather_devices())

    def on_device_removed(self, observer, device):
        """
        Fired method when a device is removed from udev
            - Delete key from GConf of the device
            - Call back observators
        """
        if device.sys_name.startswith("event"):
            try:
                device_name = device.parent["NAME"][1:-1]
                xid = XinputWarper().find_xid_by_name(device_name)
                GConfSettings().key(xid).remove()
            except KeyError:
                print ("Warning: The device parent with sys_name %s "
                       "doesn't have a NAME key." % device.sys_name)
            XinputWarper().reset_cache()

        self.__observator(self.gather_devices())
