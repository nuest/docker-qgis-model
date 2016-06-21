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

# Print out QGIS and other library versions, based on Dockerfile
echo "###### Full list of installed software:"
dpkg -l
echo "###### Installed software versions:"
python --version
gdalmanage --version
saga_cmd --version --version 2>&1 | head -1
grass --version 2>&1 | head -1
echo "Orfeo Toolbox (OTB)" $(otbcli_BandMath 2>&1 | grep 'version')
python -c 'import qgis.utils; print "QGIS: %s" % qgis.utils.QGis.QGIS_VERSION'
echo "QGIS processing plugin:" $(
cat /usr/share/qgis/python/plugins/processing/metadata.txt | grep "version")

# We expect the container is started with one model file configured via environment variable
mkdir -p $QGIS_USER_MODELDIR
echo "###### Using QGIS model file" $(ls $QGIS_MODELFILE)
cp $QGIS_MODELFILE $QGIS_USER_MODELDIR/docker.model
#cp $QGIS_MODELFILE $QGIS_USER_MODELDIR/example_analysis_linux_v2.3.model
echo "###### Model files is directory" $QGIS_USER_MODELDIR":" $(ls $QGIS_USER_MODELDIR)

# We expect the container is started with script files configured via environment variable
mkdir -p $QGIS_USER_SCRIPTDIR
if [ -f $QGIS_SCRIPTFILE ]; then
    cp $QGIS_SCRIPTFILE $QGIS_USER_SCRIPTDIR
    echo "###### Script files directory contents" $QGIS_USER_SCRIPTDIR":" $(ls $QGIS_USER_SCRIPTDIR)
fi

# Run QGIS headless, see https://marc.info/?l=qgis-developer&m=141824118828451&w=2 using X Window Virtual Framebuffer
# We except the actual model file to be configured via environment variable
echo " "
echo "###### Running model now"
xvfb-run -e $XVFB_LOGFILE python $QGIS_MODELSCRIPT

echo " "
echo "###### Data directory contents:"
tree /data

#echo " "
#echo "###### xvfb log:"
#cat $XVFB_LOGFILE

echo " "
echo "###### QGIS log:"
cat $QGIS_LOGFILE
