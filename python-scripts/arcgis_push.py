# Import libraries
import pandas as pd
from arcgis.gis import GIS
from arcgis import features
from arcgis.features import FeatureLayerCollection

# Connect to the GIS
gis = GIS("https://ddrobotec.maps.arcgis.com", "cybermax")

# Load csv from and add the csv as an item
canton_latest_csv_file = "../data-cantons-csv/dd-covid19-ch-cantons-latest.csv"
#switzerland_latest_csv_file = "../data-switzerland-csv/dd-covid19-ch-switzerland-latest.csv"

# Add the csv as an item
canton_latest_item = gis.content.get("c646a9a1727743aaa4162235d798b058")
#switzerland_latest_item = gis.content("1100451fd22d42c1bc2b18776429a8a4")

feature_layer_collection = FeatureLayerCollection.fromitem(canton_latest_item)
res = feature_layer_collection.manager.overwrite(canton_latest_csv_file)
print(res)
