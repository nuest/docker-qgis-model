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
import qgis.utils

print "### model.py ### Preparing QGIS ..."
app = QgsApplication([], True)
QgsApplication.setPrefixPath("/usr", True)
QgsApplication.initQgis()

# Enable logging
filename = os.environ['QGIS_LOGFILE']
def writelogmessage(message, tag, level):
    with open( filename, 'a' ) as logfile:
        logfile.write( '{}({}): {}\n'.format( tag, level, message ) )
QgsMessageLog.instance().messageReceived.connect( writelogmessage )

# Import and initialize Processing framework, see https://docs.qgis.org/2.8/en/docs/user_manual/processing/console.html
sys.path.append('/usr/share/qgis/python/plugins')
from processing.core.Processing import Processing
Processing.initialize()
import processing

print "### model.py ### Algorithm help and options:"
processing.alghelp("modeler:docker")
processing.algoptions("modeler:docker")

print QgsApplication.showSettings()
print "### model.py ### QGIS model prepared, logging to file %s" % filename

import datetime
from time import gmtime, strftime
from timeit import default_timer as timer
import errno

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

# Run model
inputimage_pre = os.path.join(os.environ['QGIS_WORKSPACE'], "data/jonjona_pre_conflict_proj.tif")
inputimage_post = os.path.join(os.environ['QGIS_WORKSPACE'], "data/jonjona_pos_conflict_proj.tif")

output_directory = os.path.join(os.environ['QGIS_RESULT'], datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
make_sure_path_exists(output_directory)

output_result_kmeans = os.path.join(output_directory, "result_kmeans.shp")
output_result_threshold = os.path.join(output_directory, "result_threshold.shp")
output_result_unclassified = os.path.join(output_directory, "result_unclassified.shp")

print "### model.py ### Saving output to files to\n\t" + output_result_kmeans + "\n\t" + output_result_threshold + "\n\t" + output_result_unclassified + "\n"

print "### model.py ### Start processing at " + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " ..."
start = timer()

processing.runalg("modeler:docker",inputimage_pre,inputimage_post,output_result_threshold,output_result_kmeans,output_result_unclassified)

end = timer()
print "### model.py ### Processing completed at " + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ", took " + str(end-start) + " seconds"