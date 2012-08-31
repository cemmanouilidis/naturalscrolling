# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (C) 2011 Eumorphed UG,
# Charalampos Emmanouilidis <ce@eumorphed.com>
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

# THIS IS Naturalscrolling CONFIGURATION FILE
# YOU CAN PUT THERE SOME GLOBAL VALUE
# Do not touch unless you know what you're doing.
# you're warned :)
import os


__all__ = [
    "appliation_version",
    "appliation_website",
    "get_data_file",
    "get_data_path",
    "get_locale_path",
    "get_auto_start_path",
    "get_auto_start_file_name",
    "get_auto_start_file_path",
    "get_auto_start_from_data_file_path"]

# Where your project will look for your data (for instance, images and ui
# files). By default, this is ../, relative your trunk layout
__naturalscrolling_data_directory__ = "../"
# Where your project will look for translation catalogs
__naturalscrolling_locale_directory__ = "../locales"
__version__ = "VERSION"
__website__ = "http://webiste"


class project_path_not_found(Exception):
    """Raised when we can't find the project directory."""

def appliation_version():
    return __version__


def appliation_website():
    return __website__


def get_data_file(*path_segments):
    """Get the full path to a data file.

    Returns the path to a file underneath the data directory (as defined by
    `get_data_path`). Equivalent to os.path.join(get_data_path(),
    *path_segments).
    """
    return os.path.join(get_data_path(), *path_segments)


def get_data_path():
    """Retrieve naturalscrolling data path

    This path is by default <naturalscrolling_lib_path>/../ in trunk
    and /usr/share/naturalscrolling in an installed version but this path
    is specified at installation time.
    """

    # Get pathname absolute or relative.
    path = os.path.join(
        os.path.dirname(__file__), __naturalscrolling_data_directory__)

    abs_data_path = os.path.abspath(path)
    if not os.path.exists(abs_data_path):
        print "ERROR: Unable to access the project path: %s" % abs_data_path
        raise project_path_not_found

    return abs_data_path

def get_locale_path():
    """Retrieve naturalscrolling locale path

    This path is by default <naturalscrolling_lib_path>/../locales in trunk
    and /usr/share/locale in an installed version but this path
    is specified at installation time.
    """

    # Get pathname absolute or relative.
    path = os.path.join(
        os.path.dirname(__file__), __naturalscrolling_locale_directory__)

    return os.path.abspath(path)


def get_auto_start_path():
    """ Retrieve the autostart folder from user's HOME folder """
    return os.getenv("HOME") + "/.config/autostart/"


def get_auto_start_file_name():
    """ Return the autostart file for naturalscrolling """
    return "naturalscrolling.desktop"


def get_auto_start_from_data_file_path():
    """
    Return the full path of the autostart file for naturalscrolling

    The path is hardcoded as it can't be anything else.
    """
    return "/usr/share/applications/" + get_auto_start_file_name()


def get_auto_start_file_path():
    """ Return the full path of the autostart file for naturalscrolling """
    return get_auto_start_path() + "/" + get_auto_start_file_name()
