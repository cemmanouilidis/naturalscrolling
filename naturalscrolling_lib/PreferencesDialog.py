# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

"""this dialog adjusts values in the preferences dictionary

requirements:
in module preferences: defaults[key] has a value
self.builder.get_object(key) is a suitable widget to adjust value
widget_methods[key] provides method names for the widget
each widget calls set_preference(...) when it has adjusted value
"""

import gtk
import logging
logger = logging.getLogger('naturalscrolling_lib')

from . helpers import get_builder, show_uri, get_help_uri
from . preferences import preferences

class PreferencesDialog(gtk.Dialog):
    __gtype_name__ = "PreferencesDialog"

    def __new__(cls):
        """Special static method that's automatically called by Python when 
        constructing a new instance of this class.
        
        Returns a fully instantiated PreferencesDialog object.
        """
        builder = get_builder('PreferencesNaturalscrollingDialog')
        new_object = builder.get_object("preferences_naturalscrolling_dialog")
        new_object.finish_initializing(builder)
        return new_object

    def finish_initializing(self, builder):
        """Called while initializing this instance in __new__

        finish_initalizing should be called after parsing the ui definition
        and creating a PreferencesDialog object with it in order to
        finish initializing the start of the new PerferencesNaturalscrollingDialog
        instance.
        
        Put your initialization code in here and leave __init__ undefined.
        """

        # Get a reference to the builder and set up the signals.
        self.builder = builder
        self.ui = builder.get_ui(self, True)

        # code for other initialization actions should be added here
        self.widget_methods = []

    def set_widgets_from_preferences(self):
        ''' these widgets show values in the preferences dictionary '''
        for key in preferences.keys():
            self.set_widget_from_preference(key)

    def set_widget_from_preference(self, key):
        '''set widget value from item in preferences'''

        value = preferences.get(key)
        widget = self.builder.get_object(key)
        if widget is None:
            # this preference is not adjustable by this dialog
            # for example: window and dialog geometries
            logger.debug('no widget for preference: %s' % key)
            return

        logger.debug('set_widget_from_preference: %s' % key)
        try:
            write_method_name = self.widget_methods[key][1]
        except KeyError:
            logger.warn('%s not in widget_methods' % key)
            return

        try:
            method = getattr(widget, write_method_name)
        except AttributeError:
            logger.warn("""'%s' does not have a '%s' method.
Please edit 'widget_methods' in %s"""
            % (key, write_method_name, self.__gtype_name__))
            return

        try:
            widget.connect(self.widget_methods[key][2], self.set_preference)
        except TypeError:
            logger.warn("""'%s' unknown signal name '%s'
Please edit 'widget_methods' in %s"""
            % (key, self.widget_methods[key][2], self.__gtype_name__))

        method(value)

    def get_key_for_widget(self, widget):
        key = None
        for key_try in preferences.keys():
            obj = self.builder.get_object(key_try)
            if obj == widget:
                key = key_try
        return key
 
    def set_preference(self, widget, data=None):
        '''set a preference from a widget'''
        key = self.get_key_for_widget(widget)
        if key is None:
            logger.warn('''This widget will not write to a preference.
The preference must already exist so add this widget's name
to default_preferences in your main function''')
            return

        # set_widget_from_preference is called first
        # so no KeyError test is needed here
        read_method_name = self.widget_methods[key][0]

        try:
            read_method = getattr(widget, read_method_name)
        except AttributeError:
            logger.warn("""'%s' does not have a '%s' method.
Please edit 'widget_methods' in %s"""
            % (key, read_method_name, self.__gtype_name__))
            return

        value=read_method()
        logger.debug('set_preference: %s = %s' % (key, str(value)))
        preferences[key] = value

    def on_btn_close_clicked(self, widget, data=None):
        self.destroy()

    def on_btn_help_clicked(self, widget, data=None):
        show_uri(self, "ghelp:%s" % get_help_uri('preferences'))

