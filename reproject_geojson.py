import json
from pyproj import CRS, Transformer
import os

geojson_in = 'Education_Districts.geojson'
prj_file = 'Education_Districts.prj'
geojson_out = 'Education_Districts_wgs84.geojson'

if not os.path.exists(geojson_in):
    print('GeoJSON not found:', geojson_in); raise SystemExit(1)
if not os.path.exists(prj_file):
    print('PRJ not found:', prj_file); raise SystemExit(1)

with open(prj_file, 'r', encoding='utf-8') as f:
    prj = f.read()

src_crs = CRS.from_wkt(prj)
# target CRS WGS84
tgt_crs = CRS.from_epsg(4326)
transformer = Transformer.from_crs(src_crs, tgt_crs, always_xy=True)

with open(geojson_in, 'r', encoding='utf-8') as f:
    gj = json.load(f)


def transform_coords(coords):
    # coords can be [x,y] or nested lists
    if isinstance(coords[0], (int, float)):
        x, y = coords[0], coords[1]
        lon, lat = transformer.transform(x, y)
        return [lon, lat]
    else:
        return [transform_coords(c) for c in coords]

for feat in gj.get('features', []):
    geom = feat.get('geometry')
    if not geom: continue
    geom_type = geom.get('type')
    coords = geom.get('coordinates')
    if coords is None: continue
    geom['coordinates'] = transform_coords(coords)

with open(geojson_out, 'w', encoding='utf-8') as f:
    json.dump(gj, f)

print('Wrote', geojson_out, 'features:', len(gj.get('features', [])))
