https://dipi2810x.github.io/All_Schools_Map/

Map point data:

- `2026_Schools.csv` supplies the 2026 participating-school markers.
- `Think_Tank_Organisations.csv` supplies the Think Tank organisation markers; it uses semicolon-separated `ORGANISATION`, `TOWN_AREA`, `X_COORDINATE`, and `Y_COORDINATE` columns.

Convert the district shapefiles before publishing:

```powershell
python convert_shp_to_geojson.py Education_Districts.shp -o Education_Districts.geojson
python convert_shp_to_geojson.py CT_Education_Districts.shp -o CT_Education_Districts.geojson
python reproject_geojson.py CT_Education_Districts.geojson -o CT_Education_Districts_wgs84.geojson --source-crs EPSG:32734
```
