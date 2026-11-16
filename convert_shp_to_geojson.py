"""Convert a shapefile to GeoJSON.

The CT shapefile in this repository contains geometry without a DBF sidecar,
so properties are optional. CRS conversion is handled by reproject_geojson.py.
"""
import argparse
import json
import os

import shapefile


parser = argparse.ArgumentParser()
parser.add_argument("shp", nargs="?", default="Education_Districts.shp")
parser.add_argument("-o", "--output")
args = parser.parse_args()

output = args.output or os.path.splitext(args.shp)[0] + ".geojson"
if not os.path.exists(args.shp):
    parser.error("Shapefile not found: " + args.shp)

reader = shapefile.Reader(shp=args.shp)
try:
    dbf_fields = reader.fields[1:]
except shapefile.ShapefileException:
    dbf_fields = []
fields = [field[0] for field in dbf_fields]
features = []
for index, shape in enumerate(reader.shapes(), start=1):
    props = {"feature_id": index}
    if fields:
        props.update(dict(zip(fields, reader.record(index - 1))))
    features.append({
        "type": "Feature",
        "geometry": shape.__geo_interface__,
        "properties": props
    })

with open(output, "w", encoding="utf-8") as file:
    json.dump({"type": "FeatureCollection", "features": features}, file, ensure_ascii=False)

print("Wrote", output, "features:", len(features))
