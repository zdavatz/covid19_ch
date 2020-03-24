# Import libraries
from arcgis.gis import GIS
from arcgis import features
from arcgis.features import FeatureLayerCollection
import pandas as pd
import datetime
import os

files = {
    'dd-covid19-openzh-cantons-latest.csv': '71d789eb72e8413abc6590e41a7f3cb2',
    'dd-covid19-openzh-switzerland-latest.csv': 'a48bbcb06c8e4b629a31e5584c5e991a'
    }

def file_path():
    return os.path.dirname(os.path.abspath(__file__))  + "/output_openzh/"

# Connect to the GIS
gis = GIS('https://ddrobotec.maps.arcgis.com', 'cybermax', 'hauptstrasse84!!')

for f in files:
    # Load csv from and add the csv as an item
    latest_csv_file = file_path() + f

    # Add the csv as an item using der ids
    latest_csv_item = gis.content.get(files[f])

    print("-----")

    print("Accessing feature server: " + latest_csv_item.url)
    print("Found feature layer %s on server" % latest_csv_item.title)

    #latest_csv_item.update(data=latest_csv_file)

    print("Overwriting existing feature with %s ..." % f)
    #fs = latest_csv_item.publish(overwrite=True, file_type='featureService')

    # Get feature layer collection from item
    flc = FeatureLayerCollection.fromitem(latest_csv_item)

    print(type(flc))

    # Overwrite old item with new item
    # print(latest_csv_file)
    res = flc.manager.overwrite(latest_csv_item)    
    #print(res)

