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
sys.path.append("/qgis/util")

# run preparation file http://stackoverflow.com/questions/7974849/how-can-i-make-one-python-file-run-another
import prepare

# https://docs.qgis.org/2.8/en/docs/user_manual/processing/console.html

# Import and initialize Processing framework
#from processing.core.Processing import Processing
#Processing.initialize()
import processing
import datetime

# Helper function
import os
import errno
def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

# Run model, use current time for output file name
input_image = "/data/aasee_muenster_sentinel2.tif"
output_directory = "/data/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
make_sure_path_exists(output_directory)
output_image = os.path.join(output_directory, "result.tif")

print "+++++ Start processing..."
processing.runalg("modeler:docker", input_image, output_image)
print "+++++ Processing complete"
