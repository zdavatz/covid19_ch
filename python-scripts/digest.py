import sys, getopt
import csv
import json
import urllib.request
from pathlib import Path
import os
import datetime
from common_data import *
import web

# 
# Utilities
#
def data_folder():
    return os.path.dirname(__file__)  + "/data"

def probst_folder():
    return os.path.dirname(__file__) + "/probst"

def output_folder():
    return os.path.dirname(__file__)  + "/output"

#
# Transform
#
def transform_row_openZH_data(row):
    new_row = {}
    # Mapfrom   date,time,abbreviation_canton_and_fl,ncumul_tested,ncumul_conf,ncumul_hosp,ncumul_ICU,ncumul_vent,ncumul_released,ncumul_deceased,source
    # to        date,country,abbreviation_canton,name_canton,number_canton,lat,long,hospitalized_with_symptoms,intensive_care,total_hospitalized,home_confinment,total_currently_positive_cases,new_positive_cases,recovered,deaths,total_positive_cases,tests_performed

    # Deal with inconsistent date time formats
    try:
        date_time_obj = datetime.datetime.strptime(row['date'], '%d.%m.%Y')
    except:
        date_time_obj = datetime.datetime.strptime(row['date'], '%Y-%m-%d')

    new_row['date'] = date_time_obj
    new_row['country'] = 'CH'
    canton = row['abbreviation_canton_and_fl']
    new_row['abbreviation_canton'] = row['abbreviation_canton_and_fl']
    new_row['name_canton'] = name_and_numbers_cantons[canton]['name']
    new_row['number_canton'] = name_and_numbers_cantons[canton]['number']
    new_row['lat'] = centres_cantons[canton]['lat']
    new_row['long'] = centres_cantons[canton]['lon']
    new_row['hospitalized_with_symptoms'] = 0
    new_row['intensive_care'] = row['ncumul_ICU']
    new_row['total_hospitalized'] = row['ncumul_hosp']
    new_row['home_confinment'] = 0
    new_row['total_currently_positive_cases'] = 0
    new_row['new_positive_cases'] = 0
    new_row['recovered'] = 0
    new_row['deaths'] = row['ncumul_deceased']
    new_row['total_positive_cases'] = row['ncumul_conf']
    new_row['tests_performed'] = row['ncumul_tested']

    return new_row

def transform_row_daenuprobst_data(row):
    new_row = {}

    date_time_obj = datetime.datetime.strptime(row['Date'], '%Y-%m-%d')

    new_row['date'] = date_time_obj
    new_row['country'] = 'CH'
    new_row['hospitalized_with_symptoms'] = 0
    new_row['intensive_care'] = 0
    new_row['total_hospitalized'] = 0
    new_row['home_confinment'] = 0
    new_row['total_currently_positive'] = row['CH']
    new_row['new_positive'] = 0
    new_row['recovered'] = 0
    new_row['deaths'] = 0
    new_row['total_positive'] = 0
    new_row['tests_performed'] = 0

    return new_row

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
        except:
            # no data
            print("No data for %s" % canton)
        
    return csv_path_list

def download_daenuprobst_data():
    file_path = web.download_file_to_folder(daenuprobst_csv_url, probst_folder())

#
# Digest
#
def digest_data_total_series(data_folder):
    pathlist = Path(data_folder).glob('**/*.csv')
    table = []
    for path in pathlist:
        try:
            with open(path, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    new_row = transform_row_openZH_data(row)
                    table.append(new_row)
        except:
            print("Error in " + path.name)
    
    # Sorted by time stamp
    table.sort( key = lambda e: e['date'])
    return table

def digest_daenuprobst_file(data_folder):
    path = Path(data_folder + "/covid19_cases_switzerland.csv")
    table = []
    try:
        with open(path, mode="r", encoding="utf-8-sig") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                new_row = transform_row_daenuprobst_data(row)
                table.append(new_row)
    except:
        print("Error in " + path.name)

    # Sorted by time stamp
    table.sort( key = lambda e: e['date'])
    return table
# 
# Write 
#
def write_openZH_data(table_series):
    time_series_path = os.path.join(output_folder(), "dd-covid19-ch-cantons-series.csv")
    with open(time_series_path, 'w', newline='') as csvfile:        
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(table_series)

def write_daenuprobst_data(table_series):
    file_path_switzerland = os.path.join(output_folder(), "dd-covid19-ch-switzerland-latest.csv")
    with open(file_path_switzerland, 'w', newline='') as csvfile: 
        writer = csv.DictWriter(csvfile, fieldnames=field_names_short)
        writer.writeheader()
        writer.writerows(table_series)

    file_path_cantons = os.path.join(output_folder(), "dd-covid19-ch-cantons-latest.csv")
    with open(file_path_cantons, 'w', newline='') as csvfile: 
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()


#
# Main
#
if __name__ == '__main__':
    # Download openZH data
    download_openZH_data()
    # Digest openZH data
    table_series = digest_data_total_series(data_folder())
    # Write data to csv files
    write_openZH_data(table_series)
    
    # Download Daenu Probst data
    download_daenuprobst_data()
    # Digest daenu probst data
    table_series = digest_daenuprobst_file(probst_folder())
    # Write data to csv files
    write_daenuprobst_data(table_series)
