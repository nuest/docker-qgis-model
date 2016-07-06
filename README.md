# QGIS Docker container for QGIS models

This project contains two Docker containers to run QGIS models based on a model file and a minimal Python script from the command line. The Python script contains the actual model call, using all the required input data files (which a generic script cannot guess). There are two ways to use the image. First, run it locally and mount the required script and data. Second, create a new Dockerfile to build an image that embeds the data.

The first variant is based on the QGIS Desktop container by [Kartoza](https://github.com/kartoza/docker-qgis-desktop), which is based on Debian. Thanks, Kartoza!
The second one is based on Ubuntu and UbuntuGIS repository. It was originally based on [Todd Stavish](https://github.com/toddstavish/Dockerfiles/tree/master/QGIS)'s work. Thanks, Todd!

All commands in this document are executed from within the repository's root directory.


## Example

Build the base images as described below in the section "Build the container".

Then, while in the directory `workspace/example`, run the following commands to build the image including the example data, run the container to execute the analysis, and then extract the output files to a local directory relative to the current path. The last command removes the image from local storage.

```
docker build -t qgis-model-example .
docker run --name qgis_example qgis-model-example

docker cp qgis_example:/workspace/results example_results
tree example-results
docker rm qgis_example
```

Take a look at the console - it contains several useful log statements. The directory `./example_results` contains the resulting GeoTIFF (`result.tif`) and a JPG preview file (`result.jpg`).


## Example with external data

A working example for calculating an NDVI based on a GeoTIFF is in the directory `/example`. To run it, first build the Ubuntu container and then run it with the following commands (executed from the root of this project):

```
docker build -t qgis-model-ubuntu:trusty -f ubuntu/trusty/Dockerfile ubuntu/.
docker run --rm -it -v $(pwd)/example/:/workspace qgis-model-ubuntu:trusty
```


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

Execute the following command in the directory `ubuntu` (which is the build context) to build the container and name it.

```
docker build -t qgis-model-ubuntu:<release name> ubuntu/Dockerfile.<release name> .
```

The following command builds the image for Ubuntu 14.04 and tags it as being the "latest".
Ubuntu 16.04 is still under development.

```
docker build -t qgis-model-ubuntu:trusty -t qgis-model-ubuntu:latest -f ubuntu/Dockerfile.trusty .
```

(Note the use of the `-f` parameter to set the Dockerfile, the build context is set to the directory `/ubuntu` und the `.` at the end. This was the same `model.sh` and `util` can be used for both Dockerfiles.

### Debian

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
<!--
docker run -it --rm -v /home/daniel/:/home/daniel -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=unix$DISPLAY qgis-model-runner /start.sh
-->


## Ideas/Future work

* split up the Debian image into one "QGIS plus OTB plus SAGA", and one for the model runner


## LICENSE

This project is published under the Apache License, Version 2.0.

Copyright 2016 Daniel Nüst.
