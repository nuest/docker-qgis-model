#!/bin/bash
# Copyright 2016 Daniel Nüst
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0

ROOT_DIR=$(pwd)

echo "Creating reproducibility package at" $ROOT_DIR

echo "Checking tools for creation"
git --version
npm --version
docker --version

echo "Get code, model and data for QGIS and InterIMAGE as archives"
git clone https://github.com/nuest/docker-qgis-model.git
zip -r -q qgis-model.zip docker-qgis-model
git clone https://github.com/nuest/interimage-container
zip -r -q interimage-container.zip interimage-container
rm -rf docker-qgis-model interimage-container

echo "Get kitematic fork and Docker source code, install dependencies for kitematic, and create release"
cd software
rm -rf kitematic docker
git clone https://github.com/nuest/kitematic.git
git clone https://github.com/docker/docker.git
# default branch is 'model-ui', but let's make sure:
cd kitematic
git checkout model-ui
npm install
npm run release
cd $ROOT_DIR

echo "Other software MUST be downloaded manually from the respective download sites now!"
while true; do
    read -p "Did you download all required files into the software directory? " yn
    case $yn in
        [Yy]* ) break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done

echo "Creating software.zip"
zip -r -q software.zip software
#rm -r software

echo "Make sure _no_ related images are installed"
docker rmi --force nuest/qgis-model:rs-jonjona nuest/qgis-model:xenial-multimodel nuest/interimage:1.27 nuest/interimage:latest
docker images | grep qgis-model
docker images | grep interimage

echo "Pull (download from Docker Hub) images"
docker pull nuest/qgis-model:rs-jonjona@sha256:89c9c9c00d99750ab8cb13d8633ddf45d8c992e171ca4f161ff9c8e2b5742c7c
docker pull nuest/interimage:1.27

echo "Save images to tarballs, check size and contents"
docker save --output qgis-model_rs-jonjona.tar nuest/qgis-model:rs-jonjona
tar -tvf qgis-model_rs-jonjona.tar
ls -sh qgis-model_rs-jonjona.tar
docker save --output interimage.tar nuest/interimage:1.27
tar -tvf interimage.tar
ls -sh interimage.tar

echo "Remove images again and remove potentially existing containers"
docker rmi --force nuest/qgis-model:rs-jonjona nuest/interimage:1.27
docker rm rs-jonjona

echo "Import image from serialization and run example, save the example outputs to archive"
docker load --input qgis-model_rs-jonjona.tar
docker run -it --name rs-jonjona -it nuest/qgis-model:rs-jonjona > example-analyis.log
docker cp rs-jonjona:/results example-results
tree example-results
zip -r -q example-results.zip example-results
rm -r example-results
