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
import glob
from qgis.core import *
#from qgis.gui import QgsMapCanvas
#from PyQt4.QtGui import *
import qgis.utils

print "##### Preparing..."

## Append util scripts directory to path
#sys.path.append("/qgis/util")

## Configure QApplication to fix iface issue
#qapp = QApplication([])
## Get an iface object, see http://gis.stackexchange.com/a/130483/6767
#canvas = QgsMapCanvas()
#from processing.tests.qgis_interface import QgisInterface
#iface = QgisInterface( canvas )
## Initialize the Processing plugin passing an iface object
#from processing.ProcessingPlugin import ProcessingPlugin
#plugin = ProcessingPlugin(iface)
#from processing.tools import *

qapp = QApplication([])

# https://docs.qgis.org/2.8/en/docs/user_manual/processing/console.html
# Initialize QGIS Application
app = QgsApplication([])

#QgsApplication.setPrefixPath("/usr", True)
QgsApplication.setPrefixPath("/usr/bin/qgis", True)
QgsApplication.initQgis()

# Enable logging
filename = os.environ['QGIS_LOGFILE']
def writelogmessage(message, tag, level):
    with open( filename, 'a' ) as logfile:
        logfile.write( '{}({}): {}\n'.format( tag, level, message ) )
QgsMessageLog.instance().messageReceived.connect( writelogmessage )

# http://qgis.org/api/classQgsApplication.html
print QgsApplication.showSettings()
print "###### QGIS model Docker prepared, logging to file %s" % filename

# Import and initialize Processing framework to print model metadata
from processing.core.Processing import Processing
Processing.initialize()
import processing
import datetime

print "###### Algorithm help and options:"
processing.alghelp("modeler:docker")
processing.algoptions("modeler:docker")
