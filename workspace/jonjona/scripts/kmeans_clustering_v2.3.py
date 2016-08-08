# Copyright 2016 Christian Knoth
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Author: Christian Knoth (christianknoth@uni-muenster.de)
#
# * performs  kmeans clustering from scipy on a user-defined vector layer with a user-defined number of classes
# * only uses one feature to cluster
#
# In addition to clustering, this algorithm sorts the clusters and assigns classes according to the value of the user-defined 
# feature (i.e. the class with highest number represents the cluster with the highest feature values). 
# This is done in order to be able to use the result in an automated workflow  --> The starting centroids for clusters assigned by kmeans()
# (see 'cluster' in attribute table of result) are defined by random, so the resulting cluster numbers cannot be automatically interpreted by a
# workflow.  The class numbers (see 'class' in attribute table of result) represent the clusters sorted by the feature value, so they can be 
# better integrated in automatic worflows. This mainly applies when starting centroids are distributed randomly. To increase replicability of 
# results, the method also allows for ordered centroids. In this case, starting centroids for kmeans() are distributed evenly and ordered across 
# the value range.
#
#
##input=vector
##outputLayer=output vector
##field_to_cluster=string diff_mean
##number_of_clusters=number 3
##kmeans_iterations=number 25
##random_centroids=boolean False

from qgis.core import *
import numpy as np
import math
from scipy.cluster.vq import kmeans,vq
from numpy import array
from PyQt4.QtCore import QVariant, Qt
from processing.tools.vector import VectorWriter
import os
from distutils.util import strtobool

#--------------Read vector layer--------------
inputLayer = QgsVectorLayer(input, "input layer", "ogr")


#--------------Insert attribute values into an array (based on: https://github.com/silenteddie/attributeBasedClustering/blob/master/abc_lib.py ) in order to be processed by kmeans , also check for NULL values-------------

#create empty list for attribute values to be clustered
attributeValues = []

#get features from layer
features = inputLayer.getFeatures()


# fill attribute list with attributes from features  (check for NULLs)
for feature in features:
    if feature[field_to_cluster] != NULL:
        attributeValues.append([])
        attributeValues[len(attributeValues)-1].append(feature[field_to_cluster])

# create array from attribute list
data = array(attributeValues)


# ----------------Define starting centroids and perform kmeans(). If random centroids are disabled, starting centroids are ordered and distributed evenly across the value range, otherwise random centroids are used-----------------------------
random_centroids = strtobool(os.getenv('QGIS_KMEANS_RANDOM_CENTROIDS', str(random_centroids)))
if random_centroids == False and number_of_clusters >= 2:
    #compute value range and step size for distributing the centroids 
    valueRange = np.max(attributeValues) - np.min(attributeValues)
    stepSize = valueRange/(number_of_clusters-1)
    # create array of centroids to feed into kmeans. Populate array starting with min of value range. Then proceed following stepSize and finish with max of value range. If number of clusters is 2, only min and max are used as starting centroids 
    centroidArray = np.array([[np.min(attributeValues)]])
    if number_of_clusters > 2:
        i = 1
        while i < (number_of_clusters-1):
            centroid = np.min(attributeValues)+(i*stepSize)
            centroidArray = np.append(centroidArray,[[centroid]], axis = 0)
            i+=1
    centroidArray = np.append(centroidArray,[[np.max(attributeValues)]], axis =0)
            
    #perform kmeans with starting centroids (instead of random starting centroids)
    classes,_ = kmeans(data, centroidArray)
else:
    # if random centroids are enabled, perform kmeans with random starting centroids
    classes,_ = kmeans(data, number_of_clusters, kmeans_iterations)
    

idx,_ = vq(data,classes)
idx = idx.tolist()

data


#--------------Create output layer as a copy of input layer---------------

# get fields for output layer
fields = inputLayer.pendingFields()

#create file writer
writer = QgsVectorFileWriter(outputLayer, "CP1250", fields, QGis.WKBPolygon,  inputLayer.crs(), "ESRI Shapefile")

#write features to output layer (check for NULLs)
features = inputLayer.getFeatures()

for feat in features:
     if feat[field_to_cluster] != NULL:
        writer.addFeature(feat)

del writer


#--------------Add clusters to output layer, then sort them and assign classes for the sorted clusters (from low to high, i.e. cluster with lowest values = class 0)-------------
#open output layer
vectorLayer = QgsVectorLayer(outputLayer, "kmeans output layer", "ogr")
vectorLayerDataProvider = vectorLayer.dataProvider()

# add 'cluster' field to output layer 
if vectorLayer.fieldNameIndex('cluster') == -1:
    vectorLayerDataProvider.addAttributes([QgsField('cluster', QVariant.Int)])

# add 'class' field to output layer 
if vectorLayer.fieldNameIndex('class') == -1:
    vectorLayerDataProvider.addAttributes([QgsField('class', QVariant.Int)])
    
#assign clusters
vectorLayer.updateFields()
vectorLayer.startEditing()
attrIdx = vectorLayer.fieldNameIndex('cluster')
features = vectorLayer.getFeatures()

i = 0
for feature in features:
    vectorLayer.changeAttributeValue(feature.id(), attrIdx, int(idx[i]))
    i += 1

vectorLayer.updateFields()


# -----Sort clusters and assign classes-------
attrIdx2 = vectorLayer.fieldNameIndex('class')

#create list for the max values (i.e. class boundaries) of clusters to be sorted
listOfMax = []
listOfMin = []

#iterate over clusters and find according features, then find max and min value (regarding field_to_cluster) of each cluster and add this max/min to listOfMax/listOfMin
x = 0
while x < number_of_clusters:
    exp = QgsExpression('cluster = ' + str(x))
    request = QgsFeatureRequest(exp)
    feat_subset = vectorLayer.getFeatures(request)
    valueList = []
    for feature in feat_subset:
        valueList.append(feature[field_to_cluster])
    listOfMax.append(max(valueList))
    listOfMin.append(min(valueList))
    del valueList[:]
    x+=1
    
#sort listOfMax and listOfMin
listOfMax.sort()
listOfMin.sort()

# assign class of each feature according to class boundaries given by index of sorted list (e.g. all features with value smaller or equal to the first list entry get class 0 and so on)
attrIdx2 = vectorLayer.fieldNameIndex('class')
features = vectorLayer.getFeatures()

for feature in features:
    y=0
    while y < len(listOfMax):
        if feature[field_to_cluster] <= listOfMax[y] and feature[field_to_cluster] >= listOfMin[y] : 
            vectorLayer.changeAttributeValue(feature.id(), attrIdx2, int(y))
        y+=1

vectorLayer.updateFields()
vectorLayer.commitChanges()