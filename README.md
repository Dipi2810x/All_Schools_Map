https://dipi2810x.github.io/All_Schools_Map/

Convert the district shapefiles before publishing:

```powershell
python convert_shp_to_geojson.py Education_Districts.shp -o Education_Districts.geojson
python convert_shp_to_geojson.py CT_Education_Districts.shp -o CT_Education_Districts.geojson
python reproject_geojson.py CT_Education_Districts.geojson -o CT_Education_Districts_wgs84.geojson --source-crs EPSG:32734
```
