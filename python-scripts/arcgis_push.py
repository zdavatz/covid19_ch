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

# Test data
#files = {
#    'devel-cantons-latest.csv': '0b12cddba60e49aa9ebe07c3f38cde30',
#    }

def file_path():
    return os.path.dirname(os.path.abspath(__file__))  + "/output_openzh/"

def update_from_csv(gis : GIS, f):
    # Load csv from and add the csv as an item
    latest_csv_file = os.path.join(file_path(), f)

    # Add the csv as an item using der ids
    latest_csv_item = gis.content.get(files[f])

    print("-----")

    print("Accessing feature server: " + latest_csv_item.url)
    print("Found feature layer %s on server" % latest_csv_item.title)

    print("Overwriting existing feature with %s ..." % f)

    # Get feature layer collection from item
    flc = FeatureLayerCollection.fromitem(latest_csv_item)

    print(type(flc))

    # Overwrite old item with new item
    res = flc.manager.overwrite(latest_csv_file)    
    print(res)

def publish_from_csv(gis : GIS, f : str):
    # Load csv from and add the csv as an item
    latest_csv_file = os.path.join(file_path(), f[0])

    item_prop = {'title': f.replace("-", "_").replace(".csv", "") }
    csv_item = gis.content.add(item_properties=item_prop, data=latest_csv_file)

    # publish the csv item into a feature layer
    published_item = csv_item.publish()

    print(published_item)


# Connect to the GIS
gis = GIS('https://ddrobotec.maps.arcgis.com', 'cybermax', os.environ['ARCGIS_PASS'])

for f in files:
    update_from_csv(gis, f)
