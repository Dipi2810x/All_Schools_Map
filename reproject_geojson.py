import argparse
import json
import os

from pyproj import CRS, Transformer


parser = argparse.ArgumentParser()
parser.add_argument("input", nargs="?", default="Education_Districts.geojson")
parser.add_argument("-o", "--output")
parser.add_argument("--source-crs", help="EPSG code or WKT; defaults to the matching PRJ file")
args = parser.parse_args()

output = args.output or os.path.splitext(args.input)[0] + "_wgs84.geojson"
if not os.path.exists(args.input):
    parser.error("GeoJSON not found: " + args.input)

source_crs = args.source_crs
if not source_crs:
    prj_file = os.path.splitext(args.input)[0] + ".prj"
    if not os.path.exists(prj_file):
        parser.error("Provide --source-crs when no matching PRJ file exists")
    with open(prj_file, "r", encoding="utf-8") as file:
        source_crs = file.read()

transformer = Transformer.from_crs(
    CRS.from_user_input(source_crs), CRS.from_epsg(4326), always_xy=True
)

with open(args.input, "r", encoding="utf-8") as file:
    geojson = json.load(file)

def transform_coords(coords):
    if isinstance(coords[0], (int, float)):
        x, y = coords[0], coords[1]
        lon, lat = transformer.transform(x, y)
        return [lon, lat]
    else:
        return [transform_coords(c) for c in coords]

for feature in geojson.get("features", []):
    geometry = feature.get("geometry")
    if not geometry or geometry.get("coordinates") is None:
        continue
    geometry["coordinates"] = transform_coords(geometry["coordinates"])

with open(output, "w", encoding="utf-8") as file:
    json.dump(geojson, file)

print("Wrote", output, "features:", len(geojson.get("features", [])))
