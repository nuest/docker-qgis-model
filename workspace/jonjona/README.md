
## Run command on Daniel's laptop in the git repo directory docker-qgis-model


### Build

docker build -t qgis-model-ubuntu:trusty -f ubuntu/trusty/Dockerfile ubuntu/.

docker build -t qgis-model-ubuntu:xenial -f ubuntu/xenial/Dockerfile ubuntu/.

### Run example

docker run --rm -it -v $(pwd)/example:/data qgis-model-ubuntu:trusty


### Run

docker run --rm -it -v /home/daniel/ownCloud/Reproducible-OBIA/QGIS/data-model-v2:/data qgis-model-ubuntu:trusty

#### with entrypoint 

docker run --rm -it -v /home/daniel/ownCloud/Reproducible-OBIA/QGIS/data-model-v2:/data --entrypoint /bin/bash qgis-model-ubuntu:trusty


