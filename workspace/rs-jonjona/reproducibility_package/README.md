# Reproducibility package for: Reproducibility and Practical Adoption of GEOBIA with Open-Source Software in Docker Containers

Knoth, C., Nüst, D., 2017. _Reproducibility and Practical Adoption of GEOBIA with Open-Source Software in Docker Containers_. Remote Sensing 9, 290. [doi:10.3390/rs9030290](http://dx.doi.org/10.3390/rs9030290)

## tl;dr

```bash
# QGIS
docker load --input qgis-model_rs-jonjona.tar
docker run --name rs-jonjona -it nuest/qgis-model:rs-jonjona
docker cp rs-jonjona:/results /tmp/jonjona-results
tree /tmp/jonjona-results

# InterIMAGE - Linux only!
docker load --input interimage.tar
xhost +
docker run -it --rm -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=unix$DISPLAY -e uid=$(id -u) -e gid=$(id -g) -v $(pwd):/home/data nuest/interimage:1.27 ./interimage
xhost -
```

## Contents

- `APACHE-LICENSE-2.0.txt`: full text of code license
- `cc-by-4.0-legalcode.txt`: full text of text license
- `create_package.sh`: creation script for this package
- `example-analysis.log`: log output of an example execution
- `example-results.zip`: output files an example execution
- `instructions-ui.pdf`: step by step instructions for reproducing the QGIS workflow with a user interface
- `interimage-container.zip`: source code for the InterIMAGE-based workflow (i.e. a clone of [https://github.com/nuest/interimage-container](https://github.com/nuest/interimage-container))
- `interimage.tar`: Docker image serialization (tarball) of InterIMAGE container
- `qgis-model_rs-jonjona.tar`: Docker image serialization (tarball) of QGIS container for the Jonjona use case
- `qgis-model.zip`: source code and data for the QGIS-based workflow, including Dockerfiles and the actual model (i.e. a clone of [https://github.com/nuest/docker-qgis-model](https://github.com/nuest/docker-qgis-model)
- `README.md`: this file
- `software.zip`: source code and installers for all required software in the versions current when conducting the research

## How to reproduce QGIS analysis from the paper - command line

### Software used in the analysis

The used software and detailed versions of all tools and libraries used in the OBIA method are listed in the example output log file `example-analyis.log`.

### Install software for command line reproduction

You can **install Docker Engine** based on [these online instructions](https://docs.docker.com/engine/installation/).

Just to be on the save side the software packages current when creating this package were saved in the archive `software.zip`. Docker is available as source in `software/docker` and as installers for all major platforms (`docker-engine-*.{deb,rpm,exe,pkg}`).

### Load the images

You can load the images from locally created copies (based on [docker save](https://docs.docker.com/engine/reference/commandline/save/)) with [docker load](https://docs.docker.com/engine/reference/commandline/load/).

```bash
docker load --input qgis-model_rs-jonjona.tar
```

### Start a container

```bash
docker run --name rs-jonjona -it nuest/qgis-model:rs-jonjona
```

### Extract the result files

```bash
docker cp rs-jonjona:/results /tmp/jonjona-results
tree /tmp/jonjona-results
```

You can now open the created output shapefiles (`.shp`) in your favourite GIS for further inspection.

## How to reproduce QGIS analysis from the paper - UI

### Install software for UI-based reproduction

First, install Docker Engine (see above).

Second, you can **run Kitematic** using installers or run it from source.

#### Run installed Kitematic

Install Kitematic using provided installers for Linux and Windows from the archive `software.zip` (for Linux use `Kitematic_0.12.9-amd64.deb`, for Windows extract `Kitematic-Windows.zip` and run `kitematic.exe`).

Follow the [Kitematic Instructions](https://kitematic.com/docs/) to start the software.

#### Run Kitematic from source

You can also **run Kitematic from source** using the appropriate npm and Node.js versions (easiest installed on Linux with [nvm](https://github.com/creationix/nvm), or [install version 4.1.x directly](https://nodejs.org/en/download/releases/)).

```bash
nodejs --version
cd software/kitematic
npm start
# close application with Ctrl+C
```

### Start a container from UI

In the Kitematic UI, execute the steps as described in `instructions-ui.pdf`.

## How to reproduce InterIMAGE attempts from the paper

...

## How this package was created

This package was created by the bash script `create_package.sh`, executed in the directory this README.md file is located.

## License

Code in this package is published under the Apache License, Version 2.0, unless noted otherwise.

This file is published under CC BY 4.0 ([Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/)).

Copyright 2017 [Daniel Nüst](https://github.com/nuest) and [Christian Knoth](https://www.uni-muenster.de/Geoinformatics/institute/staff/index.php/153/Christian_Knoth).
