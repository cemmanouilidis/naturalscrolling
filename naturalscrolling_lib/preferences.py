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

"""Provides a shared preferences dictionary"""

from desktopcouch.records.server import CouchDatabase
from desktopcouch.records.record import Record
import gtk
import gobject

class User_dict(dict):
    ''' a dictionary with extra methods:

    persistence: load, save and db_connect
    gobject signals: connect and emit.
    
    Don't use this directly. Please use the preferences instance.'''
    
    def __init__(self, *args, **kwds):
        dict.__init__(self, *args, **kwds)
        # Set up couchdb.
        self._db_name = "naturalscrolling"
        self._key = None
        self._database = None
        
        self._record_type = (
            "http://wiki.ubuntu.com/Quickly/RecordTypes/Naturalscrolling/"
            "Preferences")
        
        class Publisher(gtk.Invisible): # pylint: disable=R0904
            '''set up signals in a separate class
            
            gtk.Invisible has 230 public methods'''
            __gsignals__ = {'changed' : (gobject.SIGNAL_RUN_LAST,
                 gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,)),
                 'loaded' : (gobject.SIGNAL_RUN_LAST,
                 gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))}
        
        publisher = Publisher()
        self.emit  = publisher.emit
        self.connect  = publisher.connect

    def db_connect(self):
        '''connect to couchdb
        
        create if necessary'''
        # logging.basicConfig will be called now
        self._database = CouchDatabase(self._db_name, create=True)

    def save(self):
        'save to couchdb'
        self._database.update_fields(self._key, self)

 
    def load(self):
        'load from couchdb'
        self.update({"record_type": self._record_type})

        results = self._database.get_records(
            record_type=self._record_type, create_view=True)

        if len(results.rows) == 0:
            # No preferences have ever been saved
            # save them before returning.
            self._key = self._database.put_record(Record(self))
        else:
            self.update(results.rows[0].value)
            del self['_rev']
            self._key = results.rows[0].value["_id"]
        self.emit('loaded', None)

    def update(self, *args, **kwds):
        ''' interface for dictionary
        
        send changed signal when appropriate '''
        
        # parse args
        new_data = {}
        new_data.update(*args, **kwds)

        changed_keys = []
        for key in new_data.keys():
            if new_data.get(key) != dict.get(self, key):
                changed_keys.append(key)
        dict.update(self, new_data)
        if changed_keys:
            self.emit('changed', tuple(changed_keys))

    def __setitem__(self, key, value):
        ''' interface for dictionary
        
        send changed signal when appropriate '''
        if value != dict.get(self, key):
            dict.__setitem__(self, key, value)
            self.emit('changed', (key,))

preferences = User_dict()

