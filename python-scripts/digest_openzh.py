# -*- coding: utf-8 -*-

import csv
import datetime
import getopt
import json
import os
import sys
import urllib.request

import pandas as pd
import numpy as np
import pytz
import web

from pathlib import Path
from pytz import timezone
from numpy import nan
from common_data import *


utc = pytz.utc
cet = timezone('CET')

date_range = datetime.datetime.today() - start_date

def date_range_of_interest():
    return [ (start_date + datetime.timedelta(days=x)).strftime("%Y-%m-%d") for x in range(date_range.days+1)]

def data_folder():
    return os.path.dirname(os.path.abspath(__file__))  + "/data"

def output_folder():
    return os.path.dirname(os.path.abspath(__file__))  + "/output_openzh"

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
    dates = date_range_of_interest()
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

    cols = ["total_positive_cases", "tests_performed", "total_hospitalized" , "intensive_care", "deaths", "pos_tests_1", "recovered", "lat", "long", "total_currently_positive_per_100k"]

    for canton in cantons:
        per_canton_idx = canton == df['abbreviation_canton']
        df_canton = df[per_canton_idx]
        # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.fillna.html#pandas.DataFrame.fillna
        df_canton[cols] = df_canton[cols].fillna(method='ffill')
        df[per_canton_idx] = df_canton

    return df

datetime_formats = [
    "%Y-%m-%d %H:%M",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%dT%H:%M",
    "%Y-%m-%dT",
    "%Y-%m-%dT%H:%M:%S+%V:%W",
]

def parse_timestamp(d, from_time_zone=cet):
    dt = None
    for format in datetime_formats:
        try:
            dt = datetime.datetime.strptime(d, format)
            break     
        except ValueError:
            pass
    if dt == None:
        print("Error: %s could not be parsed" % d)
        return dt
    dt = datetime.datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, tzinfo=from_time_zone)
    return dt

def datetime_to_str(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S")

def convert_timestamp_string(d, from_time_zone=cet):
    dt = parse_timestamp(d, from_time_zone)
    if dt == None:
        return None
    d_utc = datetime_to_str(dt)
    return d_utc

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
    
    # Make sure we have integer types for the countable quanties
    effective_counter_columns = [item for item in df.columns if item in counter_names]

    try:
        df[ effective_counter_columns ] = df[ effective_counter_columns ].astype('Int64')
    except Exception:
        print("Cannot convert all numeric integer columns to Int64", file=sys.stderr)
        # replace non numeric types, process each numeric integer column and remove non-numeric expressions
        for c in effective_counter_columns:
            numeric = pd.to_numeric( df[ c ], errors='coerce', downcast='integer')
            df[ c ] = numeric

    # Add relative to canton population: cases / 100k
    # Generate dataframe from dictionary for easier handling
    canton_dict = pd.DataFrame.from_dict(name_and_numbers_cantons)   
    # Get all canton abbreviations
    idx = df['abbreviation_canton'].values
    # Reorder indeces
    pop_per_canton = list(canton_dict.T['pop'][idx])
    df['total_currently_positive_per_100k'] = round(100.0 * df['total_positive_cases']/pop_per_canton, 2)

    # Forward fill gaps for incremental values which might not be updated every day
    df = forward_fill_series_gaps(df)

    return df

def get_scraped_data():
    print("\nRetrieving and parsing scraper data...")
    # Get scraped csv
    header_list = ['abbreviation_canton', 'last_update', 'total_positive_cases', 'deaths', '', 'timestamp', 'source']
    functor_xyz = pd.read_csv("http://pillbox.oddb.org/current.txt", sep='\s+', engine='python', error_bad_lines=False, keep_default_na=True, header=None, names=header_list)
    functor_xyz['deaths'].replace('-', 0, inplace=True)

    # Generate pandas dataframe
    return pd.DataFrame(functor_xyz)

def generate_dataframe_from_scraped_data():
    df_xyz = get_scraped_data()

    df_xyz['last_update'] = [parse_timestamp(d, utc) for d in df_xyz['last_update']]
    df_xyz['timestamp'] = [parse_timestamp(d, utc) for d in df_xyz['timestamp']] 

    return df_xyz

def compare_two_data_frames(df1, df2):
    sum_df1 = sum(df1['total_positive_cases'])
    sum_df2 = sum(df2['total_positive_cases'])
    result = "wins"
    if sum_df1 > sum_df2:   
        print("Scraper wins: %d > OpenZH loses: %d" % (sum_df1, sum_df2))
    else:
        print("Scraper loses: %d < OpenZH wins: %d" % (sum_df1, sum_df2))

def to_int(s):
    s = s.strip()
    return int(s) if s else 0

def aggregate_latest_by_time_canton(df):
    # index set of latest entries per canton
    # Latest by date
    idx = df.groupby(['abbreviation_canton'])['date'].transform(max) == df['date']
    df = df[idx]    
    # Latest by time
    idx = df.groupby(['abbreviation_canton'])['time'].transform(max) == df['time']
    # Select rows given by index set
    return df[idx]

def aggregate_latest_by_abbrevation_canton(df):
    # Get indeces of most recent entriese
    idx = df.groupby(['abbreviation_canton'])['date'].transform(max) == df['date']   
    df = df[idx]
    # Sort according to abbreviation cantons
    df.sort_values(by=['abbreviation_canton'], inplace=True)
    df.insert(2, 'country', 'CH')

    # Now we need to move some columns
    cols = list(df)
    # Reorder columns
    cols.insert(3, cols.pop(cols.index('abbreviation_canton')))
    cols.insert(4, cols.pop(cols.index('name_canton')))
    cols.insert(5, cols.pop(cols.index('number_canton')))
    cols.insert(6, cols.pop(cols.index('lat')))
    cols.insert(7, cols.pop(cols.index('long')))
    cols.insert(12, cols.pop(cols.index('released')))
    cols.insert(13, cols.pop(cols.index('recovered')))
    cols.insert(14, cols.pop(cols.index('deaths')))
    cols.insert(15, cols.pop(cols.index('pos_tests_1')))
    cols.insert(-1, cols.pop(cols.index('source')))
    cols.insert(12, cols.pop(cols.index('total_currently_positive_per_100k')))
    df = df.loc[:, cols]
    
    df.insert(9, 'total_currently_positive_cases', df['total_positive_cases'])
    df.insert(11, 'new_positive_cases', 0)
    df.insert(16, 'ncumul_ICU_intub', 0)  # Ensures backwards compatibility, this field was removed by openzh
    
    df = df.astype({
        'tests_performed': 'Int64',
        'total_currently_positive_cases': 'Int64',
        'total_positive_cases': 'Int64',
        'new_positive_cases': 'Int64',
        'total_hospitalized': 'Int64',
        'intensive_care': 'Int64',
        'released': 'Int64',
        'recovered': 'Int64',
        'deaths': 'Int64',
        'pos_tests_1': 'Int64',
        'ncumul_ICU_intub': 'Int64',
        'ncumul_vent': 'Int64',
        'ncumul_ICF': 'Int64'
        })

    df.insert(0, 'timestamp', df['date'] + " " + df['time'])
    # Convert timestamp from CET to UTC
    df['timestamp'] = df['timestamp'].apply(convert_timestamp_string)
    df.insert(0, 'last_update', datetime.datetime.now(utc).strftime("%Y-%m-%d %H:%M:%S"))
    df.drop(columns=['date','time'], axis=1, inplace=True)

    return df

def aggregate_series_by_day_and_country(df : pd.DataFrame):
    complete_series = [(canton,x) for canton, x in df.groupby('abbreviation_canton')]
    complete_series = [ forward_fill_series_gaps(add_full_date_range(d[1], d[0])) for d in complete_series ]

    # re-assemble full series by canton
    df = pd.concat(complete_series, ignore_index = True)
    # Drop duplicate (date, canton) entries, take last of duplicates
    df.drop_duplicates(subset = ['date', 'abbreviation_canton'], keep = 'last', inplace = True, ignore_index = True)
    df.reset_index(inplace=True, drop=True)
      
    # date,country,hospitalized_with_symptoms,intensive_care,total_hospitalized,home_confinment,total_currently_positive,new_positive,released,recovered,deaths,total_positive,tests_performed
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

        total_positive = ("total_positive_cases", sum),
        tests_performed = ("tests_performed", sum),
        released = ("released", sum),
        recovered = ("recovered", sum),
        deaths = ("deaths", sum)
    ).astype('Int64')

    sum_per_day.insert(0, 'country', 'CH')  
    sum_per_day['home_confinment'] = 0
    sum_per_day['new_positive'] = sum_per_day['total_positive'].diff(periods=1).astype('Int64')
    sum_per_day['old_positive'] = sum_per_day.shift(periods=1, axis='columns', fill_value=0)['total_positive']
    sum_per_day['hospitalized_with_symptoms'] = 0

    # Reorder columns to simplify comparison with d.probst data
    sum_per_day = sum_per_day[field_names_switzerland]

    # ArcGis expects time stamps in UTC
    sum_per_day.insert(0, 'last_update', datetime.datetime.now(utc).strftime("%Y-%m-%d %H:%M:%S"))

    return sum_per_day

if __name__ == '__main__':
    # Download data from OpenZH sources
    download_openZH_data()
    # Merge tables into one time
    openzh_series = merge_openzh_data_to_series(data_folder())
    # Write to file with all data using OpenZH format
    openzh_series.to_csv(os.path.join(output_folder(), "dd-covid19-openzh-total-series.csv"), index=False)
    # Convert series to our format and decorate data with additional info
    series = convert_from_openzh(openzh_series)
    # Generate CSV
    series.to_csv(os.path.join(output_folder(), "dd-covid19-openzh-cantons-series.csv"), index=False)

    # Get newest entry for each canton
    latest_per_canton = aggregate_latest_by_time_canton(series)
    latest_per_canton.to_csv(os.path.join(output_folder(), "dd-covid19-openzh-cantons-latest-by-time.csv"), index=False)

    latest_per_canton = aggregate_latest_by_abbrevation_canton(series)
    latest_per_canton.to_csv(os.path.join(output_folder(), "dd-covid19-openzh-cantons-latest.csv"), index=False)
    # It's the same as above, but ArcGis requires unique filenames. Once a layer is created, it is very cumbersome to add new fields with ArcGis.
    latest_per_canton.to_csv(os.path.join(output_folder(), "dd-covid19-openzh-cantons-latest_v2.csv"), index=False)

    # Aggregate series over cantons for country
    country_series = aggregate_series_by_day_and_country(series)
    # Note: keep index, it's the date
    country_series.to_csv(os.path.join(output_folder(), "dd-covid19-openzh-switzerland-latest.csv"))

    # Get Baryluk data frame
    df_scraped = generate_dataframe_from_scraped_data()
    # Compare Baryluk with aggregated series
    compare_two_data_frames(df_scraped, latest_per_canton)