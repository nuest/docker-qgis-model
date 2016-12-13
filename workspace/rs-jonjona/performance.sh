#!/bin/bash
# Copyright 2016 Daniel Nüst
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0

# http://superuser.com/questions/603897/how-to-measure-average-execution-time-of-a-script
#python -m timeit --number=3 --repeat=1000000 -s 'text = "sample string"; char = "g"'  'text.find(char)'

LOOPS=2
IMAGE=nuest/qgis-model:rs-jonjona
docker pull $IMAGE

echo "Machine information"
uname -a
lscpu
sudo dmidecode -t 17

echo "Starting performance testing..."

function run_in_container {
    printf $1
    # add cpu constraints?
    docker run --rm --name performance_container_$1 $IMAGE >> containers.log 2>&1
    printf "."
}

function cleanup_containers {
    docker ps -a | grep performance | awk '{print $1}' | xargs docker rm -f
}

function container {
    i=1
    rm containers.log
    echo ""
    echo "Running image '$IMAGE' $1 times "
    while [ $i -le "$LOOPS" ]
    do
        run_in_container $i
        i=$(($i+1))
    done
    printf "\n"
    echo "Done with containers"

    #cleanup_containers
}

function run_directly {
    printf $1
    xvfb-run python model_local.py >> python.log 2>&1
    printf "."
}

function python_xvfb {
    i=1
    rm python.log
    rm qgis.log

    cp models/*.model ~/.qgis2/processing/models/
    cp scripts/*.py ~/.qgis2/processing/scripts/

    printenv >> python.log
    
    echo ""
    echo "Running Python model locally $LOOPS times"
    while [ $i -le "$LOOPS" ]
    do
        run_directly $i
        i=$(($i+1))
    done
    printf "\n"
    echo "Done with Python XVFB"
}

time container $LOOPS
time python_xvfb $LOOPS

# bash performance.sh
