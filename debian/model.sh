#!/bin/bash
# Copyright 2016 Daniel Nüst
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0

# remove previous log file if running interactive container
rm -f $QGIS_LOGFILE

# We expect the container is started with a data and model dirctory at /data
mkdir -p /root/.qgis2/processing/models
echo "Using QGIS model file" $(ls $QGIS_MODELFILE)
cp $QGIS_MODELFILE /root/.qgis2/processing/models/docker.model

# run headless: https://marc.info/?l=qgis-developer&m=141824118828451&w=2
xvfb-run python /data/model.py

echo "QGIS log:"
cat $QGIS_LOGFILE
