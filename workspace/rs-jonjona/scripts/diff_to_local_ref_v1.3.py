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

##input_layer=vector
##backup_layer=vector
##outputLayer=output vector
##field_with_superID=string set_ID
##field_with_area=string Area
##field_to_analyse=string diff_mean
##number_of_intervals=number 20


from qgis.core import *
import numpy as np
from numpy import array
import math
from PyQt4.QtCore import QVariant, Qt
from processing.tools.vector import VectorWriter



#--------------Read vector layer  to calculate reference value. Test if input is valid and has features. If not, use backup layer as input instead and enter backup mode--------------
backup = False
inputLayer = QgsVectorLayer(input_layer, "input layer", "ogr")

if not inputLayer.isValid():
    print "Layer failed to load using backup layer."
    inputLayer = QgsVectorLayer(backup_layer, "input layer", "ogr")
    backup = True

check = 0
features = inputLayer.getFeatures()
for feat in features:
    check += 1

if check == 0:
    inputLayer = QgsVectorLayer(backup_layer, "input layer", "ogr")
    backup = True
  
  
#get features from layer
features = inputLayer.getFeatures()

#create list for super-object IDs (these will be used to calculate the local reference for features in each super-object separately)
superIDs = []

# fill  list with super-object IDS from features  (check for NULLs). If in backup mode, add set all super-object IDs to 0
if backup == True:
    for feature in features:
       superIDs.append(int(0))
else:       
    for feature in features:
        if feature[field_with_superID] != NULL:
            superIDs.append(int(feature[field_with_superID]))



#--------------Create output layer as a copy of input layer --------------

# get fields for output layer
fields = inputLayer.pendingFields()

#create file writer
writer = QgsVectorFileWriter(outputLayer, "CP1250", fields, QGis.WKBPolygon,  inputLayer.crs(), "ESRI Shapefile")

#write features to output layer (check for NULLs)
features = inputLayer.getFeatures()

for feat in features:
     if feat[field_to_analyse] != NULL:
        writer.addFeature(feat)

del writer

#----------open output layer and group features in layer into specified number of intervals according to specified attribute field-------------

#open output layer
vectorLayer = QgsVectorLayer(outputLayer, "layer name you like", "ogr")
vectorLayerDataProvider = vectorLayer.dataProvider()


# add 'interval'  field to output layer 
if vectorLayer.fieldNameIndex('interval') == -1:
    vectorLayerDataProvider.addAttributes([QgsField('interval', QVariant.Int)])


vectorLayer.updateFields()
vectorLayer.startEditing()
attrIdx = vectorLayer.fieldNameIndex('interval')

if backup == True:
    features = vectorLayer.getFeatures()

#group features in layer into specified number of intervals according to specified attribute field
x = 1
while x <= max(superIDs):
    exp = QgsExpression(field_with_superID + " = " + str(x))
    request = QgsFeatureRequest(exp)
    feat_subset = vectorLayer.getFeatures(request)
    valueList = []
    for feat in feat_subset:
        valueList.append(feat[field_to_analyse])
    if len(valueList) > 0:
        valueRange = max(valueList) - min(valueList)
        intSize = float(valueRange)/number_of_intervals
        feat_subset = vectorLayer.getFeatures(request)
        for feat in feat_subset:
            if feat[field_to_analyse] == min(valueList):
                vectorLayer.changeAttributeValue(feat.id(), attrIdx, 1)
        z = 1
        while z <= number_of_intervals:
            feat_subset = vectorLayer.getFeatures(request)
            for feat in feat_subset:
                if feat[field_to_analyse] > (min(valueList)+(z-1)*intSize) and feat[field_to_analyse] <= (min(valueList)+z*intSize):
                    vectorLayer.changeAttributeValue(feat.id(), attrIdx, int(z))
            z+=1
    del valueList[:]
    x+=1


vectorLayer.updateFields()
vectorLayer.commitChanges() 



#------add 'dif_to_ref' field to layer
if vectorLayer.fieldNameIndex('dif_to_ref') == -1:
   vectorLayerDataProvider.addAttributes([QgsField('dif_to_ref', QVariant.Double)])
if vectorLayer.fieldNameIndex('local_ref') == -1:
   vectorLayerDataProvider.addAttributes([QgsField('local_ref', QVariant.Double)])



#prepare layer to add information on difference to reference
vectorLayer.updateFields()
vectorLayer.startEditing()
attrIdx2 = vectorLayer.fieldNameIndex('dif_to_ref')
attrIdx3 = vectorLayer.fieldNameIndex('local_ref')

#----------define interval covering largest area and compute mean of attributes of all features in that interval as reference value (for each super-object seperately) then compute difference to the reference for each feature -----------------

# if in backup mode, there are no super-object IDs, no intervals and local reference values (all NULL). Then diff_to_ref is simply the same value as the original value of field_to_analyse
if backup == True:
    features = vectorLayer.getFeatures()
    for feat in features:
       vectorLayer.changeAttributeValue(feat.id(), attrIdx2, feat[field_to_analyse])

x = 1
while x <= max(superIDs):
    total_areas_of_all_intervals = []
    #check if there are any objects with this superID (might not be the case, if a super-object was removed after it received an ID)
    features = vectorLayer.getFeatures(QgsFeatureRequest().setFilterExpression(u'{} = {}'.format(field_with_superID, x)))
    t=0
    for feat in features:
        t+=1
    #if there are any objects with this superID, continue...   
    if t > 0:
        y=1
        while y <= number_of_intervals:
            areas_in_interval = []
            feat_subset = vectorLayer.getFeatures(QgsFeatureRequest().setFilterExpression(u'{} = {} AND "interval" = {}'.format(field_with_superID, x, y)))
            for feat in feat_subset:
                areas_in_interval.append(feat[field_with_area])
            total_area_in_interval = sum(areas_in_interval)
            total_areas_of_all_intervals.append(total_area_in_interval)
            del areas_in_interval[:]        
            y+=1
        mode_interval = total_areas_of_all_intervals.index(max(total_areas_of_all_intervals)) + 1
        values_in_mode_interval = []
        feat_subset = vectorLayer.getFeatures(QgsFeatureRequest().setFilterExpression(u'{} = {} AND "interval" = {}'.format(field_with_superID, x, mode_interval)))
        for feat in feat_subset:
            values_in_mode_interval.append(feat[field_to_analyse])
        reference_value = (float(sum(values_in_mode_interval))/float(len(values_in_mode_interval)))
        del total_areas_of_all_intervals[:]
        del values_in_mode_interval[:]
        feat_subset = vectorLayer.getFeatures(QgsFeatureRequest().setFilterExpression(u'{} = {}'.format(field_with_superID, x)))
        for feat in feat_subset:
            dif_to_ref = feat[field_to_analyse]-reference_value
            vectorLayer.changeAttributeValue(feat.id(), attrIdx2, dif_to_ref)
            vectorLayer.changeAttributeValue(feat.id(), attrIdx3, reference_value)
            
    x+=1

vectorLayer.updateFields()
vectorLayer.commitChanges() 





