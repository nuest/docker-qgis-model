# Docker container for QGIS models

This project contains Docker containers to run [QGIS models](http://docs.qgis.org/2.0/en/docs/user_manual/processing/modeler.html) based on a model file and a minimal Python script from the command line. The Python script contains the actual model call, including all the required input data files (which a generic script cannot guess).

There are two ways to use the image. First, run it and mount the required workspacea.
Second, create a new Dockerfile to build an image that embeds the data.

There are two types of images in this repository: the first variant is based on Ubuntu and UbuntuGIS repository. It was originally based on [Todd Stavish](https://github.com/toddstavish/Dockerfiles/tree/master/QGIS)'s work. Thanks, Todd!
The second is based on the QGIS Desktop container by [Kartoza](https://github.com/kartoza/docker-qgis-desktop) (Thanks!), which is currently _not actively developed_.

_All commands in this document are executed from within the repository's root directory unless otherwise noted._


## Example workflow: NDVI

A small example workflow is contained in this repository at `workflows/example`. It calculates an [NDVI](https://en.wikipedia.org/wiki/Normalized_Difference_Vegetation_Index) for a [Sentinel satellite image](https://sentinel.esa.int/web/sentinel/sentinel-data-access) of the city center of Münster, Germany.

### With Docker Hub image

There also is an automated build [on Docker Hub](https://hub.docker.com/r/nuest/docker-qgis-model), which you can use to execute the example and then extract the result with the `docker cp` command:

```
docker run --name qgis_example nuest/docker-qgis-model:example
docker cp qgis_example:/workspace/results example_results
docker rm qgis_example
```

The following gif shows an execution of the example container.

![console gif of example execution](https://media.giphy.com/media/26BRxuXyhkReDH4dO/giphy.gif)

### With local image

Alternatively, you can build the base images as described below in the section "Build the container" and then build the example container locally.

In the directory `workspace/example`, run the following commands to build the image including the example data, run the container to execute the analysis, and then extract the output files to a local directory relative to the current path. The last command removes the image from local storage.

```
docker build -t qgis-model-example .
docker run --name qgis_example qgis-model-example

docker cp qgis_example:/workspace/results example_results
tree example-results
docker rm qgis_example
```

Take a look at the console - it contains several useful log statements. The directory `./example_results` contains the resulting GeoTIFF (`result.tif`) and a JPG preview file (`result.jpg`).

### With external data

A working example for calculating an NDVI based on a GeoTIFF is in the directory `/example`. To run it, first build the Ubuntu container and then run it with the following commands (executed from the root of this project):

```
docker build -t docker-qgis-model:trusty -f ubuntu/trusty/Dockerfile ubuntu/.
docker run --rm -it -v $(pwd)/example/:/workspace qgis-model-ubuntu:trusty
```

Or using the image from Docker Hub:

```
docker run --name qgis_example_hub -v <path to>/workspace/example/:/workspace nuest/docker-qgis-model:trusty
```

### With OSGeo-Live or local Linux OS

The [OSGeo-Live](http://live.osgeo.org/en/index.html) DVD or VM, also have all software you need to execute the workflow. If you use QGIS under Linux, this might even work on your own desktop computer.

If you want to give the example a try with OSGeo-Live, [download](http://live.osgeo.org/en/download.html) and start it and run the following commands in a terminal.
The steps are: clone the repository, copy the model file to the required location, and run the model:

```
git clone https://github.com/nuest/docker-qgis-model.git
cd docker-qgis-model/workspace/example
cp models/compute_NDVI.model ~/.qgis2/processing/models/docker.model
python model.py
```

Take a look at the data in the directory `/tmp/results/<current datetime>` (the full path is contained in the logs shown in the console).

To make this work, the file `model.py` uses default values for some of the environment variables that are originally defined in the Dockerfile.

## Preparations to package a workflow

Prepare a directory with the following contents. In the remainder of these instructions, we will assume it is called `data`.

* `/models/*.model` - your QGIS workflow model (one only, or configure name via environment variable `QGIS_MODELFILE`)
  * when the container is executed, this file is copied into the model directory of the root user under the name `model.docker` so that it must be referenced in the python file as `"modeler:docker"`
* `model.py` - a minimal Python file with the run command referencing the required data files, see template below. Depending on your model, the actual call to `processing.runalg(...)` will look very different. For example, it might container several inputs and/or outputs.
* all data files
* any additional user scripts in `scrips/*.py`

**Python file template:**

```
#!/usr/bin/python

# Run preparation file
import sys
sys.path.append("/qgis/util")
import prepare

# Import and initialize Processing framework
from processing.core.Processing import Processing
Processing.initialize()
import processing

# Run model
input="/workspace/data/input.file"
output="/workspace/data/output.file"

print "Start processing..."
processing.runalg("modeler:docker",input,output)
print "Processing complete"
``` 


## Run the model with a mounted workspace

Build the container (see below) and start it with the following command, mounting your `workspace` directory to `/workspace` and replacing `<platform>` with either `debian` or `ubuntu`. In the latter case we recommend to explicitly select the Ubuntu version and thereby the QGIS version by appending either the tag `:trusty` or `:xenial`. If you want to publish your whole model in a self-contained image, see next section.

```
docker run --rm -it -v /<path to workspace dir>:/workspace qgis-model-<platform>
```

### Configuration

If you want to run the model manually (i.e. to debug etc.) append `/bin/bash` to the command to override the default command, then execute `./qgis/model.sh` manually.

The used options are as follows:
* `--rm` will remove the container as soon as it ends
* `-it` ensures you can see the stdout logs
* The startup script will copy all files named `*.model` from the mounted directory

Potentially useful additional options are as these:
* `--name="qgis"` to name the running container for easier identification
* To *execute a specific model*, you can overwrite the environment variable `QGIS_MODELFILE` which has the default value `/workspace/models/*.model`. This is useful if you have a working directory with more than one model file. Specify the environment variable when you run the container: `docker run --rm -it -v /<path to workspace dir>:/workspace -e QGIS_MODELFILE=/workspace/models/mymodel.model qgis-model-<platform>`
* If you want to run the model manually (i.e. to debug etc.) add the parameter `--entrypoint=/bin/bash` to the command (before the image name) to override the default entrypoint and get a bash shell, then execute `./qgis/model.sh` manually.

### Access log while running

After the model has started you can access the current state of the containers log file with the command `docker exec`:

```
docker ps
# note the name of the container running the command /qgis/model.sh
docker exec <container name> cat /qgis/qgis.log
```

Alternatively to `cat`, you can use `less` or any other tools available in the container.


## Create a self-contained image

The previous run command mounts a directory of the host computer to the container, which is suitable for model development. If you want to publish a self-contained Docker image, you can create a minimal Dockerfile based on the images created above, which simply copies your data into the container, then build and execute that image.

Be aware that you to access the output of the process you must not use `--rm` but keep the container to extract the data and delete it afterwards. See above in section "Example with embedded data" for the required commands.


## Build the container

### Ubuntu

See directory `/ubuntu/Dockerfile.<release name>` for the respective Dockerfile

Execute the following command in the root directory `/` of this repository to build the container and name it.

```
docker build -t docker-qgis-model:<release name> -f ubuntu/Dockerfile.<release name> ./ubuntu
```

The build context is set to `./ubuntu`, the Dockerfile name is configured explicitly.

The following command, executed from within the directory `/ubuntu`, builds the image for Ubuntu 14.04 and tags it as being the "latest".
Ubuntu 16.04 is still under development.

```
docker build -t docker-qgis-model:trusty -t qgis-model-ubuntu:latest -f Dockerfile.trusty .
```

Note the use of the `-f` parameter to set the Dockerfile, which does not have the default name. The build context is set to the directory `/ubuntu` und the `.` at the end. This was the same `model.sh` and `util` can be used for both Dockerfiles.

### [WIP] Debian

* See directory `/debian` for the Dockerfile
* http://kartoza.com/qgis-desktop-in-docker/
* https://github.com/kartoza/docker-qgis-desktop/tree/develop/2.14
  * mounts X11 (and dis/enables xhost, for minimum security)

Execute the following command to build the container and name it.

```
docker build -t qgis-model-debian debian/.
```

You can also run an interactive version of this container (with QGIS user interface) by adding the following parameters to the `docker run` call, for details see [the base images starth.sh script](https://github.com/kartoza/docker-qgis-desktop/blob/develop/2.14/start.sh).

```
xhost +local:docker
docker run -it --rm -v /<path to user home>:/home/<user name> -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=unix$DISPLAY qgis-model-debian /start.sh
xhost -local:docker
```


## LICENSE

This project is published under the Apache License, Version 2.0.

Copyright 2016 Daniel Nüst.
