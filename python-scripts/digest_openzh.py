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
from numpy import nan

date_range = datetime.datetime.today() - start_date

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

def set_canton_info(df):
    cantons_col = df['abbreviation_canton']

    # Generate additional columns
    df['lat'] = list(map(lambda name: centres_cantons[name]['lat'], cantons_col ))
    df['long'] = list(map(lambda name: centres_cantons[name]['lon'], cantons_col ))
    df['name_canton'] = list(map(lambda name: name_and_numbers_cantons[name]['name'], cantons_col ))
    df['number_canton'] = list(map(lambda name: name_and_numbers_cantons[name]['number'], cantons_col ))

    return df

def add_full_date_range(df, canton):
    dates = [ (start_date + datetime.timedelta(days=x)).strftime("%Y-%m-%d") for x in range(date_range.days)]
    existing_dates = df['date']

    # TODO: loop is very slow, probably better to use something like pd.concat()
    print("Please be patient...")
    for d in dates:
        if d not in existing_dates:
            df = df.append( {"date" : d}, ignore_index=True )

    df.sort_values(by=["date"], inplace = True)
    df.reset_index(inplace=True, drop=True)

    df['abbreviation_canton'] = canton

    df = set_canton_info(df)

    return df

def merge_openzh_data_to_series(data_folder):
    pathlist = Path(data_folder).glob('**/*.csv')
    openzh_data_frames = []
    for path in pathlist:
        try:
            new_data_frame = pd.read_csv(path)
            # Drop duplicate date entries, take last of duplicates
            new_data_frame.drop_duplicates(subset = 'date', keep = 'last', inplace = True, ignore_index = True)
            openzh_data_frames.append(new_data_frame)
        except Exception as e:
            print("Error in %s: %s" % (path.name, e))
    
    openzh_data_frame = pd.concat(openzh_data_frames, ignore_index=True)
    openzh_data_frame = openzh_data_frame.sort_values(by=["date", "abbreviation_canton_and_fl"])

    openzh_data_frame.reset_index(inplace=True, drop=True)

    return openzh_data_frame

def forward_fill_series_gaps(df):
    cantons = list(df['abbreviation_canton'].unique())

    cols = ["total_positive_cases", "tests_performed", "total_hospitalized" , "intensive_care", "deaths", "pos_tests_1", "recovered", "lat", "long"]

    for canton in cantons:
        per_canton_idx = canton == df['abbreviation_canton']
        df_canton = df[per_canton_idx]
        # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.fillna.html#pandas.DataFrame.fillna
        df_canton[cols] = df_canton[cols].fillna(method='ffill')
        df[per_canton_idx] = df_canton

    return df

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

    # Replace time NaN values with valid time in order to sort
    df['time'] = df['time'].fillna('00:00')

    # Forward fill gaps for incremental values which might not be updated every day
    df = forward_fill_series_gaps(df)

    return df

def to_int(s):
    s = s.strip()
    return int(s) if s else 0

def aggregate_latest_by_canton(df):
    # index set of latest entries per canton
    # Latest by date
    idx = df.groupby(['abbreviation_canton'])['date'].transform(max) == df['date']
    df = df[idx]    
    # Latest by time
    idx = df.groupby(['abbreviation_canton'])['time'].transform(max) == df['time']
    # Select rows given by index set
    return df[idx]

def aggregate_series_by_day_and_country(df : pd.DataFrame):
    complete_series = [(canton,x) for canton, x in df.groupby('abbreviation_canton')]
    complete_series = [ forward_fill_series_gaps(add_full_date_range(d[1], d[0])) for d in complete_series ]

    # re-assemble full series by canton
    df = pd.concat(complete_series, ignore_index = True)
    # Drop duplicate (date, canton) entries, take last of duplicates
    df.drop_duplicates(subset = ['date', 'abbreviation_canton'], keep = 'last', inplace = True, ignore_index = True)
    df.reset_index(inplace=True, drop=True)

    # date,country,hospitalized_with_symptoms,intensive_care,total_hospitalized,home_confinment,total_currently_positive,new_positive,recovered,deaths,total_positive,tests_performed
    sum_per_day = df.groupby(
        ['date']
    ).agg(
        # Not present in source data
        # hospitalized_with_symptoms = ("hospitalized_with_symptoms", sum),
        intensive_care = ("intensive_care", sum),
        total_hospitalized = ("total_hospitalized", sum),
        # Not present in source data
        # home_confinment = ("home_confinment", sum),
        
        # Not sure what the difference is to total_positive_cases
        total_currently_positive = ("total_positive_cases", sum),

        # TODO: compute new positive on full time series
        # new_positive = ("new_positive", sum),
        recovered = ("recovered", sum),
        deaths = ("deaths", sum),
        total_positive = ("total_positive_cases", sum),
        tests_performed = ("tests_performed", sum)
    )

    sum_per_day['country'] = 'CH'    

    return sum_per_day

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

    # Aggregate series over cantons for country
    country_series = aggregate_series_by_day_and_country(series)
    # Note: keep index, it's the date
    country_series.to_csv(os.path.join(output_folder(), "dd-covid19-ch-switzerland-latest.csv"))
