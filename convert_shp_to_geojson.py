import shapefile
import json
import os

shp = 'Education_Districts.shp'
out = 'Education_Districts.geojson'

if not os.path.exists(shp):
    print('Shapefile not found:', shp)
    raise SystemExit(1)

r = shapefile.Reader(shp)
fields = [f[0] for f in r.fields[1:]]
features = []
for sr in r.shapeRecords():
    geom = sr.shape.__geo_interface__
    props = dict(zip(fields, sr.record))
    features.append({
        'type': 'Feature',
        'geometry': geom,
        'properties': props
    })

fc = { 'type': 'FeatureCollection', 'features': features }
with open(out, 'w', encoding='utf-8') as f:
    json.dump(fc, f, ensure_ascii=False)

print('Wrote', out, 'features:', len(features))
