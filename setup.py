#!/usr/bin/env python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (C) 2011 Eumorphed UG,
# Charalampos Emmanouilidis <ce@eumorphed.com>
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 3, as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranties of
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.
### END LICENSE

###################### DO NOT TOUCH THIS (HEAD TO THE SECOND PART) ###########

import os
import sys

try:
    import DistUtilsExtra.auto
except ImportError:
    print >> sys.stderr, ("To build naturalscrolling you need "
                          "https://launchpad.net/python-distutils-extra")
    sys.exit(1)
assert DistUtilsExtra.auto.\
        __version__ >= "2.18", "need DistUtilsExtra >= 2.18"


def update_config(values={}):
    oldvalues = {}
    try:
        fin = file("naturalscrolling_lib/naturalscrollingconfig.py", "r")
        fout = file(fin.name + ".new", "w")

        for line in fin:
            fields = line.split(" = ") # Separate variable from value
            if fields[0] in values:
                oldvalues[fields[0]] = fields[1].strip()
                line = "%s = \"%s\"\n" % (fields[0], values[fields[0]])
            fout.write(line)

        fout.flush()
        fout.close()
        fin.close()
        os.rename(fout.name, fin.name)
    except (OSError, IOError):
        print("ERROR: Can't find "
              "naturalscrolling_lib/naturalscrollingconfig.py")
        sys.exit(1)
    return oldvalues


def update_desktop_file(datadir):
    try:
        fin = file("naturalscrolling.desktop", "r")
        fout = file(fin.name + ".new", "w")

        for line in fin:
            if "Icon=" in line:
                line = "Icon=%s\n" % (datadir + "media/naturalscrolling.svg")
            fout.write(line)
        fout.flush()
        fout.close()
        fin.close()
        os.rename(fout.name, fin.name)
    except (OSError, IOError):
        print "ERROR: Can't find naturalscrolling.desktop"
        sys.exit(1)


class InstallAndUpdateDataDirectory(DistUtilsExtra.auto.install_auto):

    def run(self):
        path = self.prefix + "/share/naturalscrolling/"
        values = {"__naturalscrolling_data_directory__": path,
                  "__version__": self.distribution.get_version(),
                  "__license__": self.distribution.get_license(),
                  "__website__": self.distribution.get_url()}
        previous_values = update_config(values)
        update_desktop_file(path)
        DistUtilsExtra.auto.install_auto.run(self)
        update_config(previous_values)


##############################################################################
###################### YOU SHOULD MODIFY ONLY WHAT IS BELOW ##################
##############################################################################

DistUtilsExtra.auto.setup(
    name="naturalscrolling",
    version="0.5.0",
    license="GPL-3",
    author="Charalampos Emmanouilidis",
    author_email="charalampos.emmanouilidis@eumorphed.com",
    description="Natural Scrolling for Linux",
    long_description=("Natural Scrolling adds a menu bar item allowing the "
                      "direction of scrolling to be toggled"),
    url="https://github.com/cemmanouilidis/naturalscrolling",
    cmdclass={"install": InstallAndUpdateDataDirectory},
    data_files=[("share/naturalscrolling/", ["naturalscrolling.desktop"]),
                ("share/naturalscrolling/media", ["media/Screenshot.png",
                    "media/natural-scrolling-status-activated.png",
                    "media/natural-scrolling-status-not-activated.png",
                    "media/naturalscrolling.svg"])])
