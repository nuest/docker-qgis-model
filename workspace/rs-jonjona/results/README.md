# rs-jonjona workflow outputs

This workspace creates three output files:

- `settlements.shp` - shapefile with polygons of detected settlement areas
- `result_unclassified.shp` - shapefile with polygons of all detected objects; objects contain calculated parameters:
  - `diff_mean`: change in edge intensity
  - `Set_ID`: membership to settlement
  - `dif_to_ref`: difference to local reference regarding change
  - `local_ref`: local reference value for the whole settlement
  - `dif_class`: clustering result, one of three classes of which 2 has the highest change values
  - `cl_ratio`: ratio of cell value pre-morphological-filtering to post-filtering, which is used to remove interfering objects
- `result_threshold.shp` - shapefile with locations of objects detected as changed based on a user-defined threshold