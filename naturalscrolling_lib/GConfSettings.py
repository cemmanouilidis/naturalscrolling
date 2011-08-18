# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (C) 2011 Guillaume Hain <zedtux@zedroot.org>
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

import gconf

## GConf setup

# GConf root path
GCONF_ROOT_DIR = "/apps/naturalscrolling"

# Natural Scrolling keys path definition
GCONF_NATURAL_SCROLLING_KEY = GCONF_ROOT_DIR + "/natural_scrolling"

# Natural Scrolling keys type definition
gconf_keys = {GCONF_NATURAL_SCROLLING_KEY: bool}


## Exception classes
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
            cls._instance = super(GConfServer, cls).__new__(
                cls, *args, **kwargs
            )
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
    
    def on_settings_changed(self, client, timestamp, entry, *extra):
        """
        This is the callback function that is called when the keys in our
        namespace change (such as editing them with gconf-editor).
        """
        key = entry.get_key()
        if not key in gconf_keys:
            raise InvalidKey("Unknown key %s" % key)
        
        if not key in self.__key_update_observators:
            return
        
        # Execute observer's method passing GConf key value as parameter
        self.__key_update_observators[key](entry.get_value().get_bool())
    
class GConfKey(object):
    
    def __init__(self, key):
        if not key in gconf_keys:
            raise InvalidKey("Unknown key %s" % key)
        
        self.__gconf = GConfServer().client
        self.__value = None
        self.__key = key
        self.__type = gconf_keys[key]
        self.get_value()
    
    def get_value(self):
        """
        Magic method to read the value from GConf (auto cast)
        """
        if self.__type == bool:
            self.__value = self.__gconf.get_bool(self.__key)
        elif self.__type == str:
            self.__value = self.__gconf.get_string(self.__key)
        elif self.__type == int:
            self.__value = self.__gconf.get_int(self.__key)
        else:
            raise InvalidKeyType("Invalid key type %s" % self.__type)
    
    def set_value(self):
        """
        Magic method to write the value to GConf (auto cast)
        """
        if self.__type == bool:
            self.__gconf.set_bool(self.__key, self.__value)
        elif self.__type == str:
            self.__gconf.set_string(self.__key, self.__value)
        elif self.__type == int:
            self.__gconf.set_int(self.__key, self.__value)
        else:
            raise InvalidKeyType("Invalid key type %s" % self.__type)
    
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

class GConfSettings(object):
    
    def server(self):
        """
        Return the Singleton instance of the GConfServer
        """
        return GConfServer()
    
    def key(self, key):
        """
        Ruby styled method to define which is the key to check
        This method return an instance of the GConfKey class
        otherwise raise a InvalidKey or InvalidKeyType
        """
        return GConfKey(key)
