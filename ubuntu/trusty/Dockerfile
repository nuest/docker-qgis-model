# Copyright 2016 Daniel Nüst
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
FROM ubuntu:14.04
MAINTAINER Daniel Nüst <daniel.nuest@uni-muenster.de>

# For ubuntu 14.04, potentially useful for 16.04 as well:
# Add qgis repos to get latest QGIS, see https://www.qgis.org/en/site/forusers/alldownloads.html#debian-ubuntu/qgis.org
# use the one with ubuntugis dependencies > http://qgis.org/ubuntugis/

RUN apt-get update \
    && apt-get install -qqy software-properties-common --no-install-recommends \
    && apt-add-repository -y ppa:ubuntugis/ubuntugis-unstable \ 
    && apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 314DF160 \
    && apt-get -qqy update \
    && apt-get install -qqy --no-install-recommends \
        tree \
        xvfb \
        # QGIS requirements:
        gdal-bin \
        otb-bin \
        otb-bin-qt \
        python-otb \
        python-qgis-common \
        python-qgis \
        #saga \
        grass \
        # Python installer; numerical and imaging libs:
        python-pip \
        python-dev \
        python-scipy \
        python-numpy \
        libjpeg8-dev \
        # QGIS:
        qgis-plugin-grass \
        qgis-providers \
        qgis \
        python-qgis \
        # Needed to compile SAGA:
        wget \
        g++ \
        make \
        automake \
        libtool \
        libwxgtk3.0-dev \
        libtiff5-dev \
        libtiff4-dev \
        libgdal-dev \
        libproj-dev \
        libjasper-dev \
        libexpat1-dev \
        wx-common \
        libogdi3.2-dev \
        unixodbc-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install SAGA in specific version to avoid compatibility issues: http://hub.qgis.org/issues/13279
# A manualy try using software-properties-common and devscripts (rmadison) from different source packages/repos shows many different versions, but explicitly installing 2.2.0+dfsg-1build2 or 2.1.4+dfsg-1ubuntu1 does NOT work
# Instructions based on https://sourceforge.net/p/saga-gis/wiki/Compiling%20a%20Linux%20Unicode%20version/
ENV SAGA_VERSION_MINOR 2.2.0
ENV SAGA_VERSION 2.2
RUN wget http://downloads.sourceforge.net/project/saga-gis/SAGA%20-%20$SAGA_VERSION/SAGA%20$SAGA_VERSION_MINOR/saga_$SAGA_VERSION_MINOR.tar.gz \
    && tar -xvzf saga*.tar.gz

WORKDIR saga-$SAGA_VERSION_MINOR
RUN ./configure \
    && make \
    && make install
    
#RUN pip install Pillow GDAL

ENV PYTHONPATH=/usr/share/qgis/python:/usr/lib/otb/python:/usr/share/qgis/python/plugins
ENV QGIS_LOGFILE=/qgis/qgis.log
ENV QGIS_MODELFILE=/data/models/*.model
ENV QGIS_SCRIPTFILE=/data/scripts/*.py
ENV QGIS_USER_MODELDIR=/root/.qgis2/processing/models
ENV QGIS_USER_SCRIPTDIR=/root/.qgis2/processing/scripts
ENV QGIS_MODELSCRIPT=/data/model.py
ENV XVFB_LOGFILE=/qgis/xvfb.log

# Add main script
WORKDIR /qgis
COPY model.sh model.sh
RUN chmod 0755 model.sh

ENTRYPOINT ["/qgis/model.sh"]
