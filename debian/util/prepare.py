#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2016 Daniel Nüst
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
import sys
import os
from qgis.core import *

# Append qgis to path
sys.path.append("/qgis/util")

# https://docs.qgis.org/2.8/en/docs/user_manual/processing/console.html

# Initialize QGIS Application
QgsApplication.setPrefixPath("/usr/bin/qgis", True)
app = QgsApplication([], True)
QgsApplication.initQgis()

# Enable logging
filename = os.environ['QGIS_LOGFILE']
def writelogmessage(message, tag, level):
    with open( filename, 'a' ) as logfile:
        logfile.write( '{}({}): {}\n'.format( tag, level, message ) )
QgsMessageLog.instance().messageReceived.connect( writelogmessage )

# http://qgis.org/api/classQgsApplication.html
print QgsApplication.showSettings()
print "QGIS model Docker prepared, logging to file %s" % filename
