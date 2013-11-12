#!/usr/bin/env python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Charalampos Emmanouilidis <chrys.emmanouilidis@gmail.com>
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
                line = "%s = \"%s\"\n" % (fields[0], values[fields[0]].strip('"'))
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
        data_path = self.prefix + "/share/naturalscrolling/"
        locale_path = self.prefix + "/share/locale/"
        values = {"__naturalscrolling_data_directory__": data_path,
                  "__naturalscrolling_locale_directory__": locale_path,
                  "__version__": self.distribution.get_version(),
                  "__license__": self.distribution.get_license(),
                  "__website__": self.distribution.get_url()}
        previous_values = update_config(values)
        update_desktop_file(data_path)
        DistUtilsExtra.auto.install_auto.run(self)
        update_config(previous_values)
        update_desktop_file("")


##############################################################################
###################### YOU SHOULD MODIFY ONLY WHAT IS BELOW ##################
##############################################################################

DistUtilsExtra.auto.setup(
    name="naturalscrolling",
    version="0.7.0",
    license="GPL-3",
    author="Charalampos Emmanouilidis",
    author_email="chrys.emmanouilidis@gmail.com",
    description="Natural Scrolling for Linux",
    long_description=("Natural Scrolling adds a menu bar item allowing the "
                      "direction of scrolling to be toggled"),
    url="https://github.com/cemmanouilidis/naturalscrolling",
    cmdclass={"install": InstallAndUpdateDataDirectory},
    data_files=[("/usr/share/applications/", ["naturalscrolling.desktop"]),
                ("share/naturalscrolling/media", ["media/Screenshot.png",
                    "media/natural-scrolling-status-activated.png",
                    "media/natural-scrolling-status-not-activated.png",
                    "media/naturalscrolling.svg"]),
                ("share/locale/cs_CZ/LC_MESSAGES", ["locales/cs_CZ/LC_MESSAGES/naturalscrolling.mo"]),
                ("share/locale/es_ES/LC_MESSAGES", ["locales/es_ES/LC_MESSAGES/naturalscrolling.mo"]),
                ("share/locale/fr_FR/LC_MESSAGES", ["locales/fr_FR/LC_MESSAGES/naturalscrolling.mo"]),
                ("share/locale/it_IT/LC_MESSAGES", ["locales/it_IT/LC_MESSAGES/naturalscrolling.mo"]),
                ("share/locale/nl_NL/LC_MESSAGES", ["locales/nl_NL/LC_MESSAGES/naturalscrolling.mo"]),
                ("share/locale/pt_BR/LC_MESSAGES", ["locales/pt_BR/LC_MESSAGES/naturalscrolling.mo"]),
                ("share/locale/sv_SV/LC_MESSAGES", ["locales/sv_SV/LC_MESSAGES/naturalscrolling.mo"])
                ]
)
