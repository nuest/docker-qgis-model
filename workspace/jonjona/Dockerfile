# Copyright 2016 Daniel Nüst
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
FROM nuest/qgis-model:xenial
MAINTAINER Daniel Nüst <daniel.nuest@uni-muenster.de>

COPY . /workspace

LABEL de.ifgi.qgis-model.options '[ \
    { "id": "MODEL_INPUT_1", \
      "name": "first setting", \
      "value": "100", \
      "comment": "this is a comment for the first setting" }, \
    { "id": "MODEL_INPUT_2", \
      "name": "second setting", \
      "value": "huge" }, \
    { "id": "MODEL_INPUT_RAND_CENTROIDS", \
      "name": "Random centroids for k-Means", \
      "value": "false", \
      "comment": "If the centroids are non-random for the k-Means algorithm, the results are reproducible between model runs." }]'

# Execute the following commands _in the directory of this file_ to build and execute a self-contained image:
# BUILD COMMAND: docker build -t qgis-model-jonjona .
# RUN COMMAND: docker run --name jonjona -it qgis-model-jonjona
# Extract results: docker cp jonjona:/workspace results
# RUN with random centroids:
#   docker run --name jonjona-random qgis-model-jonjona -e "QGIS_KMEANS_RANDOM_CENTROIDS=true"
#   docker cp jonjona-random:/workspace results/random 