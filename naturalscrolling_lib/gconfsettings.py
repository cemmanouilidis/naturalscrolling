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

import re
import gconf

## GConf setup

# GConf root path
GCONF_ROOT_DIR = "/apps/naturalscrolling"


class InvalidKey(Exception):
    """ Raised class when key is unknown """


class InvalidKeyType(Exception):
    """ Raised class when key type is unknown """


class GConfServer(object):
    # Singleton
    _instance = None
    _init_done = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(GConfServer, cls).__new__(cls, *args,
                                                                 **kwargs)
        return cls._instance

    def __init__(self):
        """
        Open connection to GConf
        and connect to callback on naturalscrolling keys updates
        """
        if self._init_done:
            return

        if not hasattr(self, "__key_update_observators"):
            self.__key_update_observators = {}

        if not hasattr(self, "__keys_update_observators"):
            self.__keys_update_observators = []

        if not hasattr(self, "client"):
            # Get GConf client:
            self.client = gconf.client_get_default()

            # Add the root directory to the list of directories that our GConf
            # client will watch for changes:
            self.client.add_dir(GCONF_ROOT_DIR, gconf.CLIENT_PRELOAD_NONE)

            # Assign a callback function for when changes are made to keys in
            # the root directory namespace:
            self.client.notify_add(GCONF_ROOT_DIR, self.on_settings_changed)

        self._init_done = True

    def fire_me_when_update_on_key(self, key, method):
        """
        Register a Class instance method to fire
        swhen the given an update on the given key have been catched
        """
        self.__key_update_observators[key] = method

    def on_update_fire(self, method):
        """
        Register method to fire when a key of the GConf root path
        has been updated
        """
        self.__keys_update_observators.append(method)

    def on_settings_changed(self, client, timestamp, entry, *extra):
        """
        This is the callback function that is called when the keys in our
        namespace change (such as editing them with gconf-editor).
        """
        # Do nothing when the key has been removed
        if not entry.value:
            return

        key = entry.key
        gconf_key = GConfKey(key, entry.value.type)
        self.execute_callback_on_observers(key, gconf_key)

    def execute_callback_on_observers(self, key, gconf_key):
        if key in self.__key_update_observators:
            # Execute observer's method passing GConf key value as parameter
            self.__key_update_observators[key](gconf_key.get_value())

        if self.__keys_update_observators:
            for observator in self.__keys_update_observators:
                observator(gconf_key.name, gconf_key.get_value())

    def entries(self):
        """
        Return a list of all entries from naturalscrolling root path
        """
        return self.client.all_entries("/apps/naturalscrolling")


class GConfKey(object):

    class KeyDoesntExits(Exception):
        pass

    def __init__(self, key, type=None):
        self.__gconf = GConfServer().client
        self.__value = None

        if key.startswith(GCONF_ROOT_DIR):
            self.__key = key
            self.__name = self._without_root_path(key)
        else:
            self.__key = self._with_root_path(key)
            self.__name = key

        if type:
            self.__type = type
        else:
            try:
                self.__type = self.__gconf.get(self.__key).type
            except AttributeError:
                raise GConfKey.KeyDoesntExits(_("Can't find the key '%s'") %
                                              self.__key)

    def get_name(self):
        return self.__name
    name = property(get_name)

    def _without_root_path(self, key):
        return re.sub("%s/" % GCONF_ROOT_DIR, "", key)

    def _with_root_path(self, key):
        return "%s/%s" % (GCONF_ROOT_DIR, key)

    def get_value(self):
        """
        Magic method to read the value from GConf (auto cast)
        """
        if self.__type == gconf.VALUE_BOOL:
            return self.__gconf.get_bool(self.__key)
        elif self.__type == gconf.VALUE_STRING:
            return self.__gconf.get_string(self.__key)
        elif self.__type == gconf.VALUE_INT:
            return self.__gconf.get_int(self.__key)
        else:
            raise InvalidKeyType(_("Can't read the value for type '%s'") %
                                 self.__type)

    def set_value(self, value):
        """
        Magic method to write the value to GConf (auto cast)
        """
        if self.__type == gconf.VALUE_BOOL:
            self.__gconf.set_bool(self.__key, value)
        elif self.__type == gconf.VALUE_STRING:
            self.__gconf.set_string(self.__key, value)
        elif self.__type == gconf.VALUE_INT:
            self.__gconf.set_int(self.__key, value)
        else:
            raise InvalidKeyType(_("Can't write the value '%s'"
                                   " for type '%s'") % (value, self.__type))

    def is_enable(self):
        return self.__value == True

    def enable(self):
        """
        Set a boolean key value to True
        """
        self.__value = 1
        self.set_value()

    def disable(self):
        """
        Set a boolean key value to False
        """
        self.__value = 0
        self.set_value()

    def find_or_create(self):
        """
        Check if the current instance of GConfKey exists otherwise create it
        """
        if not self.__gconf.get(self.__key):
            self.set_value(False)

    def remove(self):
        """ Remove the key from GConf """
        self.__gconf.unset(self.__key)


class GConfSettings(object):

    def server(self):
        """
        Return the Singleton instance of the GConfServer
        """
        return GConfServer()

    def initialize(self, devices):
        """
        Check if all keys exists
        Create missing keys
        """
        for device in devices:
            if not device.keys()[0]:
                print (_("Warning: The XID of the device with name %s "
                       "wasn't found") % device.values()[0])
            else:
                gconf_key = GConfKey(device.keys()[0], gconf.VALUE_BOOL)
                gconf_key.find_or_create()

                # As you're in the initializing step, if there is at least one
                # observator, then fire it with all the actual configuration
                self.server().execute_callback_on_observers(device.keys()[0],
                                                            gconf_key)

    def key(self, key, type=None):
        """
        Ruby styled method to define which is the key to check
        This method return an instance of the GConfKey class
        otherwise raise a InvalidKey or InvalidKeyType
        """
        return GConfKey(key, self.python_type_to_gconf_type(type))

    def python_type_to_gconf_type(self, type):
        """
        Convert a Python type (bool, int, str, ...) to GConf type
        """
        if type == bool:
            return gconf.VALUE_BOOL
        elif type == str:
            return gconf.VALUE_STRING
        elif type == int:
            return gconf.VALUE_INT

    def keys(self):
        """
        Return a list of all keys for natural scrolling
        """
        return GConfServer().client.all_entries(GCONF_ROOT_DIR)

    def activated_devices_xids(self):
        """
        Return a list of all XIDs of devices where naturalscrolling was
        registered as activated.
        """
        activated_devices_xids = []
        for entry in self.server().entries():
            try:
                gconf_key = GConfKey(entry.key)
                if gconf_key.get_value():
                    activated_devices_xids.append(gconf_key.name)
            except GConfKey.KeyDoesntExits:
                # Pass the removed key
                pass
        return activated_devices_xids
