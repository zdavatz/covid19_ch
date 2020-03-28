# Import libraries
from arcgis.gis import GIS
from arcgis import features
from arcgis.features import FeatureLayerCollection
from copy import deepcopy
import pandas as pd
import numpy as np
import datetime
import os

files = {
    'dd-covid19-openzh-cantons-latest.csv': '71d789eb72e8413abc6590e41a7f3cb2',
    'dd-covid19-openzh-cantons-latest_v2.csv': 'fa069dd8882e4b93b7ce29ebbbd9808d',
    'dd-covid19-openzh-switzerland-latest.csv': 'a48bbcb06c8e4b629a31e5584c5e991a',
    'dd-covid19-openzh-cantons-series.csv': '06e0afde23f54da5be4a49cbc8c9d80b'
    }

canton_file_name = 'dd-covid19-openzh-cantons-latest_v2.csv'
geojson_file_id = 'a3d3c27946b34671b25ef6d49e480315'

# Test data
'''
files = {
    'dd-covid19-openzh-switzerland-latest.csv': 'a48bbcb06c8e4b629a31e5584c5e991a'
    }
'''

def file_path():
    return os.path.dirname(os.path.abspath(__file__))  + "/output_openzh/"

def update_geojson_file(gis: GIS):
    # Load canton csv from file
    csv_file_path = os.path.join(file_path(), canton_file_name)
    csv = pd.read_csv(csv_file_path)
    # Create dictionary name_canton -> tot_currently_positive_per_100k
    tot_pos_cases_per_100k = dict(zip(csv['name_canton'], csv['total_currently_positive_per_100k']))

    # Get geojson file item
    geojson_file_item = gis.content.get(geojson_file_id)

    print("-----")
    print("Accessing feature server: " + geojson_file_item.url)
    print("Found feature layer %s on server" % geojson_file_item.title)

    # Assume the first layer is the layer you want to update
    fl = geojson_file_item.layers[0]
    # Get feature set and corresponding features
    fset = fl.query()
    features = fset.features
    # Loop through all features and set tot_pos_cases
    for feature in features:
        name = feature.get_value('name')
        tot_pos_100k = tot_pos_cases_per_100k[name]
        feature.set_value('tot_pos_cases_per_100k', tot_pos_100k)
    
    # Update online feature layer
    results = fl.edit_features(updates=features)

def update_fields_from_csv(gis: GIS, f, latest_csv_item):
    # Load csv from and add the csv as an item
    latest_csv_file = os.path.join(file_path(), f)

    layer = latest_csv_item.layers[0]

    # Get the existing list of fields on the cities feature layer
    fields = layer.manager.properties.fields

    field_names = [ n["name"] for n in fields ]

    print("Existing fields %s" % field_names)

    new_data = pd.read_csv(latest_csv_file)

    new_column_names = list(new_data.columns)

    columns_to_add = [ n for n in new_column_names if n not in field_names ]

    print("New fields %s" % columns_to_add)

    # get a template field
    template_field = dict(deepcopy(fields[5]))

    fields_to_be_added = []
    for new_field_name in columns_to_add:
        current_field = deepcopy(template_field)
        if new_data.dtypes[new_field_name] == np.int64:
            current_field['sqlType'] = 'sqlTypeInteger'
            current_field['type'] = 'esriFieldTypeInteger'
            current_field['name'] = new_field_name.lower()
            current_field['alias'] = new_field_name
            fields_to_be_added.append(current_field)
        elif new_data.dtypes[new_field_name] == np.float:
            current_field['sqlType'] = 'sqlTypeFloat'
            current_field['type'] = 'esriFieldTypeDouble'
            current_field['name'] = new_field_name.lower()
            current_field['alias'] = new_field_name
            fields_to_be_added.append(current_field)

    print("Adding field specs: %s" % fields_to_be_added)
    result = layer.manager.add_to_definition({'fields':fields_to_be_added})
    print(result)

def update_fields_in_switzerland_latest_file(f, item):
    # Load csv from and add the csv as an item
    latest_csv_file = os.path.join(file_path(), f)
    # Read data
    df = pd.read_csv(latest_csv_file)
    # Assume the first layer is the layer you want to update
    fl = item.layers[0]

    # Get a template field
    fields = fl.manager.properties.fields    
    if not 'doubling_time_total_positive' in [f['name'] for f in fields]:
        template_field = dict(deepcopy(fields[10]))
        template_field['name'] = 'doubling_time_total_positive'
        template_field['type'] = 'esriFieldTypeDouble'
        template_field['alias'] = 'doubling_time_total_positive'
        template_field['nullable'] = True
        template_field['visible'] = True
        template_field['editable'] = True
        template_field['sqlType'] = 'sqlTypeOther'
        template_field['default_value'] = 0.0
        res = fl.manager.add_to_definition({'fields': [template_field]})    
        print(res)

    # Check if fiels was successfully added
    fields = fl.manager.properties.fields    
    for field in fields:
        print(f"{field.name:30}|  {field.type}")

    # Get feature set and corresponding features
    fset = fl.query()
    features = fset.features
   
    # Loop through all features and set doubling_time
    for feature in features:
        # Get date string
        date = datetime.datetime.fromtimestamp(feature.attributes['date']/1000)
        date_str = date.strftime("%Y-%m-%d")
        idx = df['date'] == date_str
        # Get doubling time
        doubling_time_total_positive = df.loc[idx]['doubling_time_total_positive'].values[0]
        # Update individual feature
        feature.set_value('doubling_time_total_positive', doubling_time_total_positive)

    print("Updating all existing features with %s ..." % f)
    # Update online feature layer
    return fl.edit_features(updates=features)   

def update_from_csv(gis: GIS, f):
    # Load csv from and add the csv as an item
    latest_csv_file = os.path.join(file_path(), f)

    # Add the csv as an item using der ids
    latest_csv_item = gis.content.get(files[f])

    print("-----")
    print("Accessing feature server: " + latest_csv_item.url)
    print("Found feature layer %s on server" % latest_csv_item.title)

    # Get feature layer collection from item
    flc = FeatureLayerCollection.fromitem(latest_csv_item)
    print(type(flc))

    print("Overwriting existing feature with %s ..." % f)
    # Overwrite old item with new item
    res = flc.manager.overwrite(latest_csv_file)
    print(res)

    # TODO: not working, the overwrite below removes the new field names again
    # update_fields_from_csv(gis, f, latest_csv_item)
    if f == 'dd-covid19-openzh-switzerland-latest.csv':   
        print("Updating existing feature with %s ..." % f)
        res = update_fields_in_switzerland_latest_file(f, latest_csv_item)

def publish_from_csv(gis : GIS, f : str):
    # Load csv from and add the csv as an item
    latest_csv_file = os.path.join(file_path(), f[0])

    item_prop = {'title': f.replace("-", "_").replace(".csv", "") }
    csv_item = gis.content.add(item_properties=item_prop, data=latest_csv_file)

    # publish the csv item into a feature layer
    published_item = csv_item.publish()

    print(published_item)


# Connect to the GIS
if __name__ == '__main__':
    gis = GIS('https://ddrobotec.maps.arcgis.com', 'cybermax', os.environ['ARCGIS_PASS'])

    for f in files:
       update_from_csv(gis, f)

    update_geojson_file(gis)