# -*- coding: utf-8 -*-

import sys, getopt
import csv
import json
import urllib.request
from pathlib import Path
import os
import datetime
from common_data import *
import pandas as pd
import web

def data_folder():
    return os.path.dirname(__file__)  + "/data"

def output_folder():
    return os.path.dirname(__file__)  + "/output"

def download_openZH_data():
    csv_path_list = []
    for canton in centres_cantons:
        try:
            if canton != 'FL':
                filename = openZH_per_canton_format % canton
            else:
                filename = openZH_per_country_format % canton

            file_path = web.download_file_to_folder(openZH_base_url + filename, data_folder())
            csv_path_list.append(file_path)
        except Exception as e:
            # no data
            print("No data for %s: %s" % (canton, e))
        
    return csv_path_list

def merge_openzh_data_to_series(data_folder):
    pathlist = Path(data_folder).glob('**/*.csv')
    openzh_data_frames = []
    for path in pathlist:
        try:
            new_data_frame = pd.read_csv(path)
            openzh_data_frames.append(new_data_frame)
        except Exception as e:
            print("Error in %s: %s" % (path.name, e))
    
    openzh_data_frame = pd.concat(openzh_data_frames, ignore_index=True)
    openzh_data_frame = openzh_data_frame.sort_values(by=["date", "abbreviation_canton_and_fl"])

    openzh_data_frame.reset_index(inplace=True, drop=True)

    #with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.max_colwidth', -1):  # more options can be specified also
    #print(openzh_data_frame)
    
    return openzh_data_frame

def convert_from_openzh(df):
    # Rename 1:1 columns
    cols = df.columns    
    new_cols = map( lambda name : openzh_field_mapping[name] if name in openzh_field_mapping.keys() else name, cols  )
    df.columns = new_cols

    cantons_col = df['abbreviation_canton']

    # Generate additional columns
    df['lat'] = list(map(lambda name: centres_cantons[name]['lat'], cantons_col ))
    df['long'] = list(map(lambda name: centres_cantons[name]['lon'], cantons_col ))
    df['name_canton'] = list(map(lambda name: name_and_numbers_cantons[name]['name'], cantons_col ))
    df['number_canton'] = list(map(lambda name: name_and_numbers_cantons[name]['number'], cantons_col ))

    return df

def to_int(s):
    s = s.strip()
    return int(s) if s else 0

def aggregate_latest_by_canton(df):
    # index set of latest entries per canton
    idx = df.groupby(['abbreviation_canton'])['date'].transform(max) == df['date']
    # Select rows given by index set
    return df[idx]

if __name__ == '__main__':
    # Download data from OpenZH sources
    download_openZH_data()
    # Merge tables into one time
    openzh_series = merge_openzh_data_to_series(data_folder())
    # Write to file with all data using OpenZH format
    openzh_series.to_csv(os.path.join(output_folder(), "openzh_total_series-latest.csv"), index=False)
    # Convert series to our format and decorate data with additional info
    series = convert_from_openzh(openzh_series)
    series.to_csv(os.path.join(output_folder(), "dd-covid19-ch-cantons-series.csv"), index=False)

    # Get newest entry for each canton
    latest_per_canton = aggregate_latest_by_canton(series)
    latest_per_canton.to_csv(os.path.join(output_folder(), "dd-covid19-ch-cantons-latest.csv"), index=False)
