# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

'''facade - makes naturalscrolling_lib package easy to refactor

while keeping its api constant'''
from . helpers import set_up_logging
from . preferences import preferences
from . Window import Window
from . naturalscrollingconfig import get_version

