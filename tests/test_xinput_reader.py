#!/usr/bin/python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (C) 2011 Eumorphed UG, Charalampos Emmanouilidis <ce@eumorphed.com>
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

import os
import sys
import unittest
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), "..")))

from naturalscrolling_lib import SwissKnife

class TestXinputReader (unittest.TestCase):
    def setUp(self):
        self.testdir     = os.path.dirname (os.path.abspath (__file__))
        self.testdatadir = '%s/data/xinput/' % self.testdir
        self.testfiles   = [
            ['xinput_one_slave_pointer.txt'  , 1],
            ['xinput_two_slave_pointer.txt'  , 2],
            ['xinput_three_slave_pointer.txt', 3],
            ['xinput_six_slave_pointer.txt'  , 6],
            ['xinput_seven_slave_pointer.txt', 7],
        ]

    
    def testGetNrOfSlavePointer (self):
        reader = SwissKnife.XinputReader()

        for f in self.testfiles:
            file_abs_path = os.path.abspath ('%s/%s' % (self.testdatadir, f[0]))
            
            xinput_list_output = ''.join (open (file_abs_path, 'r').readlines())
            expected_nr_of_devices = f[1]
            
            slavepointer = reader.get_slave_pointer (xinput_list_output)
            self.assertTrue (len (slavepointer) == expected_nr_of_devices, 'Failed to detect number of slave pointer for file %s' % file_abs_path)


    def testXinputListCommand (self):
        xinput = SwissKnife.Xinput()
        xinput_list_output = xinput.list()
        
        self.assertTrue (len (xinput_list_output) > 0, 'empty output for command <xinput list>')


if __name__ == '__main__':    
    unittest.main()
