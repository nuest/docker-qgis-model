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
import tempfile
import glob
import datetime
from time import gmtime, strftime
from timeit import default_timer as timer

from qgis.core import *
import qgis.utils

print "##### Preparing..."
# Initialize QGIS Application > https://docs.qgis.org/2.8/en/docs/user_manual/processing/console.html
app = QgsApplication([], True)
QgsApplication.setPrefixPath("/usr", True)
QgsApplication.initQgis()
print "##### QgsApplication initialized."

# Enable logging
logfilename = os.getenv('QGIS_LOGFILE', os.path.join(tempfile.gettempdir(), 'qgis.log'))
def writelogmessage(message, tag, level):
    with open( logfilename, 'a' ) as logfile:
        logfile.write( '{}({}): {}\n'.format( tag, level, message ) )
QgsMessageLog.instance().messageReceived.connect( writelogmessage )
print "##### QGIS logs to file %s" % logfilename

print "##### QGIS settings:"
print QgsApplication.showSettings()

# Import and initialize Processing framework
sys.path.append('/usr/share/qgis/python/plugins')
from processing.core.Processing import Processing
Processing.initialize()
import processing

print "###### Algorithm help and options:"
processing.alghelp("modeler:docker")
processing.algoptions("modeler:docker")

# Helper function for creating output directory
import errno
def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

# Run model, use current timestamp for output directory name
input_image = os.path.join(os.getenv('QGIS_WORKSPACE', os.getcwd()), "aasee_muenster_sentinel2.tif")
output_directory = os.path.join(os.getenv('QGIS_RESULT', os.path.join(tempfile.gettempdir(), 'results')), datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
make_sure_path_exists(output_directory)
output_image = os.path.join(output_directory, "result.tif")

print "###### Saving output to file to\t\t" + output_image

print "###### Start processing at " + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " ..."
start = timer()

processing.runalg("modeler:docker", input_image, output_image)

end = timer()
print "###### Processing complete at " + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ", took " + str(end-start) + " seconds"

print "###### Output image info:"
os.system("gdalinfo " + output_image)


output_preview = os.path.join(output_directory, "result.jpg")
os.system("gdal_translate -of JPEG -scale " + output_image + " " + output_preview)
print "###### Created jpg preview for result.tif"
