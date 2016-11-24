# Jonjona change analysis

## Run it

```bash
docker run -it --name jonjona nuest/qgis-model:rs-jonjona
docker cp jonjona:/workspace .
```

## Analysis parameters

- `settlement_threshold`
  - settlement detection sensitivity: the standard deviation that an image segment/image object is used as a seed for a settlement
  - default: `0.3`
- `settlement_size`
  - minimum settlement size: the minimal size for a settlement candidate after grow and merge of seeds
  - unit: `m²`
  - default: `0`
- `change_analysis_threshold`
  - change sensitivity: minimum change in edge intensity for objects to be flagged as changed
  - default: `0.3`