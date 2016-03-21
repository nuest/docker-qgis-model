# Copyright 2016 Daniel Nüst
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
FROM toddstavish/qgis
MAINTAINER Daniel Nüst <daniel.nuest@uni-muenster.de>

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    xvfb \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONPATH=/usr/share/qgis/python:/usr/lib/otb/python:/usr/share/qgis/python/plugins
ENV QGIS_LOGFILE=/qgis/qgis.log
ENV QGIS_MODELFILE=/data/*.model
ENV QGIS_USER_MODELDIR=/root/.qgis2/processing/models
ENV QGIS_MODELSCRIPT=/data/model.py

# Add main script
WORKDIR /qgis
COPY model.sh model.sh
RUN chmod 0755 model.sh

COPY util util

ENTRYPOINT ["/qgis/model.sh"]
