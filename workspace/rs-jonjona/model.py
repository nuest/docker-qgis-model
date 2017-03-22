#!/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: skip-file

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

import warnings; # Silence the error "UserWarning: Matplotlib is building the font cache using fc-list. This may take a moment.", see https://github.com/matplotlib/matplotlib/issues/5836#issuecomment-179592427
with warnings.catch_warnings():
    warnings.simplefilter("ignore"); 
    from processing.core.Processing import Processing
    from processing.core.Processing import ProcessingConfig

Processing.initialize()
import processing

# Manually set the OTB path, see https://github.com/qgis/QGIS/blob/master/python/plugins/processing/core/ProcessingConfig.py and https://github.com/qgis/QGIS/blob/master/python/plugins/processing/algs/otb/OTBUtils.py
ProcessingConfig.setSettingValue("OTB_FOLDER", os.getenv('OTB_FOLDER', ''))
ProcessingConfig.setSettingValue("OTB_LIB_FOLDER", os.getenv('OTB_LIB_FOLDER', ''))

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

# Debug model info
print "### model.py ### Algorithm help and options for model"
qgis_model_name = "modeler:example_analysis_linux_v3.2"
processing.alghelp(qgis_model_name)
processing.algoptions(qgis_model_name)

print QgsApplication.showSettings()
print "### model.py ### QGIS model prepared, logging to file %s" % filename

# Run model
inputimage_pre = os.path.join(os.environ['QGIS_WORKSPACE'], "data/pre_conflict.tif")
inputimage_post = os.path.join(os.environ['QGIS_WORKSPACE'], "data/post_conflict.tif")

output_directory = os.path.join(os.environ['QGIS_RESULT'], datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
make_sure_path_exists(output_directory)

output_settlements = os.path.join(output_directory, "settlements.shp")
output_result_unclassified = os.path.join(output_directory, "result_unclassified.shp")
output_result_threshold = os.path.join(output_directory, "result_threshold.shp")
print "### model.py ### Saving output to files to\n\t" + output_settlements + "\n\t" + output_result_unclassified + "\n\t" + output_result_threshold + "\n"

settlement_threshold = os.getenv('settlement_threshold', 0.3)
settlement_size = os.getenv('settlement_size', 0)
change_analysis_threshold = os.getenv('change_analysis_threshold', 0.33)
print "### model.py ### Input paramters:\n\tsettlement detection sensitivity: " + str(settlement_threshold) + "\n\tminimum settlement size: " + str(settlement_size) + "\n\tchange sensitivity: " + str(change_analysis_threshold) + "\n"

print "### model.py ### Start processing at " + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " ..."
start = timer()

processing.runalg(qgis_model_name,
    inputimage_pre,
    inputimage_post,
    change_analysis_threshold,
    settlement_threshold,
    settlement_size,
    output_settlements,
    output_result_threshold,
    output_result_unclassified)

end = timer()
print "### model.py ### Processing completed at " + strftime("%Y-%m-%d %H:%M:%S", gmtime()) + ", took " + str(end-start) + " seconds"