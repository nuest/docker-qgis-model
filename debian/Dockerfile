# Copyright 2016 Daniel Nüst
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
FROM kartoza/qgis-desktop:2.8
MAINTAINER Daniel Nüst <daniel.nuest@uni-muenster.de>

RUN apt-get -y update \
	&& apt-get install -y --no-install-recommends \
	software-properties-common \
	&& add-apt-repository ppa:johanvdw/saga-gis \
	&& apt-get install -y --no-install-recommends \
	saga \
	nano \
    python-qt4-sql \
	python-gdal \
	python-psycopg2 \
	# for building OTB, if in base image then comment out
	build-essential \
	qt4-dev-tools \
	libqt4-core \
	libqt4-dev \
	# can also use SuperBuild instead of following list of deps
	libboost1.55-dev \
	zlib1g-dev \
	libopencv-dev \
	##curl \
    ##libcurl4-openssl-dev \
	libmapnik-dev \
	swig \
	libpython-dev \
	libgeotiff-dev \
	#libinsighttoolkit4.6 \ is only available in version 3.20.1, but 4.6.0 is minimum version
	#libossim is only available in version 1.8.16-3 for jessie, but 1.8.20-3 is required
	libopenthreads-dev \
	libtinyxml2.6.2 \
	libtinyxml-dev \
	libfftw3-bin \
	libfftw3-dev \
	libsvm3 \
	libsvm-dev \
	libfreetype6 \
	libkml0 \
	libkml-dev \
	patchelf \
	libboost-graph-dev \
	libboost-regex-dev \
	libexpat1-dev \
	libjpeg-turbo-progs \
	libpcre3 \
	libpcre3-dev \
	libc6 \
	libc6-dev \
	makeself \
	libtool \
	libgeos-dbg \
	libgeos++-dev

# https://hub.docker.com/r/toddstavish/orfeo_toolbox/~/dockerfile/ does not work because I cannot use ubuntugis
# http://jordiinglada.net/wp/2015/05/27/installing-otb-has-never-been-so-easy-8/ and https://www.orfeo-toolbox.org//SoftwareGuide/SoftwareGuidech2.html#x14-190002 and http://wiki.orfeo-toolbox.org/index.php/QGIS_access_to_OTB_applications#Notes_for_Debian.2FUbuntu_users
WORKDIR /otb
RUN git clone https://git@git.orfeo-toolbox.org/git/otb.git
# try without super build by adding the dependencies above
#	&& curl -OL https://www.orfeo-toolbox.org/packages/SuperBuild-archives-trunk.tar.bz2 \
#	&& tar xvjf SuperBuild-archives-trunk.tar.bz2
# Take parameter names from https://github.com/orfeotoolbox/OTB/tree/master/SuperBuild/CMake
WORKDIR /otb/build
RUN mkdir /otb/install \
	&& cmake -D CMAKE_INSTALL_PREFIX:PATH=/otb/install \
	-D USE_SYSTEM_GDAL:BOOL=ON \
	-D USE_SYSTEM_TIFF:BOOL=ON \
	-D USE_SYSTEM_GEOTIFF:BOOL=ON \
	-D USE_SYSTEM_JPEG:BOOL=ON \
	-D USE_SYSTEM_EXPAT:BOOL=ON \
	-D USE_SYSTEM_FFTW:BOOL=ON \
	-D USE_SYSTEM_TINYXML:BOOL=ON \
	-D USE_SYSTEM_LIBKML:BOOL=ON \
	-D USE_SYSTEM_LIBSVM:BOOL=ON \
	-D USE_SYSTEM_OPENCV:BOOL=ON \
	-D USE_SYSTEM_CURL:BOOL=ON \
	-D USE_SYSTEM_BOOST:BOOL=ON \
	-D USE_SYSTEM_GEOS:BOOL=ON \
	-D USE_SYSTEM_OPENTHREADS:BOOL=ON \
	-D USE_SYSTEM_FREETYPE:BOOL=ON \
	/otb/otb/SuperBuild \
	&& make
# muparser not available in required version
# ossim version in jessie is too old
# itk version in jessie is too old

# copy created binaries where they belong
WORKDIR /otb/install
RUN cp -r lib /usr
RUN cp bin/* /usr/bin/

# path to qgis, qgis python plugins, and OTB
ENV PYTHONPATH=/usr/share/qgis/python:/usr/lib/otb/python:/usr/share/qgis/python/plugins
ENV QGIS_LOGFILE=/qgis/qgis.log
ENV QGIS_MODELFILE=/data/*.model

# add main script
WORKDIR /qgis
COPY model.sh model.sh
RUN chmod 0755 model.sh
COPY util util

CMD ["/qgis/model.sh"]
#CMD ["/start.sh"]

## TODO try out wget https://www.orfeo-toolbox.org/packages/OTB-5.2.1-Linux64.run && bash OTB*.run and take it from there...
