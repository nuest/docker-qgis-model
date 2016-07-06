##input=vector
##outputLayer=output vector
##field_to_cluster=string diff_mean
##number_of_clusters=number 3
##kmeans_iterations=number 25

from qgis.core import *
from qgis.gui import QgsMapCanvas
from PyQt4.QtGui import *

import numpy as np
import math
from scipy.cluster.vq import kmeans,vq
from numpy import array
from PyQt4.QtCore import QVariant, Qt
from processing.tools.vector import VectorWriter
from processing.core.ProcessingLog import ProcessingLog

logtag = "kmeans_clustering_v2.3"
# MessageLevel { INFO = 0, WARNING = 1, CRITICAL = 2 }
QgsMessageLog.logMessage("Starting", logtag, QgsMessageLog.INFO)


#--------------read vector layer--------------
inputLayer = QgsVectorLayer(input, "input layer", "ogr")
QgsMessageLog.logMessage("Read input layer with " + str(inputLayer.featureCount()) + " features.", logtag, QgsMessageLog.INFO)


#--------------insert attribute values into an array in order to be processed by kmeans() , based on [...]--------------

#create empty list for attribute values to be clustered
attributeValues = []

#get features from Layer
features = inputLayer.getFeatures()

# fill attribute list with attributes from features  (check for NULLs)
for feature in features:
    if feature[field_to_cluster] != NULL:
        attributeValues.append([])
        attributeValues[len(attributeValues)-1].append(feature[field_to_cluster])

# create array fom attribute list
data = array(attributeValues)
QgsMessageLog.logMessage("Data array size: " + str(data.shape), logtag, QgsMessageLog.INFO)


#---------------if only 3 classes are chosen, perform kmeans clustering with 3 clusters using fix and ordered starting centroids (in order to make the results directly interpretable, i.e. class 1 < class 2 < class 3) else perform kmeans with random starting centroids--------------
#TODO: make more flexible by ordering resulting clusters instead of input centroids

if number_of_clusters == 3:
    #get  min, median and max of values and use as starting centroids 
    QgsMessageLog.logMessage("#clusters is " + str(number_of_clusters) + " - kmeans chosen starting centroids (min, median, max) for reproducibility", logtag, QgsMessageLog.INFO)
    startingCentroid1 = np.min(attributeValues)
    startingCentroid2 = np.median(attributeValues)
    startingCentroid3 = np.max(attributeValues)
    centroidArray = np.array([[startingCentroid1],[startingCentroid2],[startingCentroid3]])
    #perform kmeans with starting centroids (instead of random starting centroids)
    classes,_ = kmeans(data, centroidArray)
else:
    #perform kmeans with random starting centroids
    QgsMessageLog.logMessage("#clusters is " + str(number_of_clusters) + " - kmeans with random starting centroids", logtag, QgsMessageLog.INFO)
    classes,_ = kmeans(data, number_of_clusters, kmeans_iterations)


idx,_ = vq(data,classes)
idx = idx.tolist()


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


#--------------add classes to ouput layer--------------
#open output layer
vectorLayer = QgsVectorLayer(outputLayer, "layer name you like", "ogr")
vectorLayerDataProvider = vectorLayer.dataProvider()


# add 'class' field to output layer and assign classes
if vectorLayer.fieldNameIndex('class') == -1:
    vectorLayerDataProvider.addAttributes([QgsField('class', QVariant.Int)])

vectorLayer.updateFields()
vectorLayer.startEditing()
attrIdx = vectorLayer.fieldNameIndex('class')
features = vectorLayer.getFeatures()

i = 0
for feature in features:
    vectorLayer.changeAttributeValue(feature.id(), attrIdx, int(idx[i]))
    i += 1

vectorLayer.updateFields()
vectorLayer.commitChanges()
QgsMessageLog.logMessage("Created output layer with " + str(vectorLayer.featureCount()) + " features.", logtag, QgsMessageLog.INFO)

QgsMessageLog.logMessage("Done", logtag, QgsMessageLog.INFO)