import sys, getopt
import csv
import json
import urllib.request
from pathlib import Path
import os
import datetime


# Latest data per canton and for Switzerland
# Using data provided by the Statistische Amt, Kanton Zuerich on Github
# https://github.com/openZH/covid_19

openZH_base_url = 'https://raw.githubusercontent.com/openZH/covid_19/master/fallzahlen_kanton_total_csv/'
openZH_per_canton_format = 'COVID19_Fallzahlen_Kanton_%s_total.csv'
openZH_per_country_format = 'COVID19_Fallzahlen_%s_total.csv'

# Latest data per canton 
# https://github.com/daenuprobst/covid19-cases-switzerland
daenuprobst_csv_url = "https://raw.githubusercontent.com/daenuprobst/covid19-cases-switzerland/master/covid19_cases_switzerland.csv"


field_names = "date,country,abbreviation_canton,name_canton,lat,long,hospitalized_with_symptoms,intensive_care,total_hospitalized,home_confinment,total_currently_positive_cases,new_positive_cases,recovered,deaths,total_positive_cases,tests_performed".split(',')

#
# Centres of cantons
# 
# Thanks to https://github.com/daenuprobst
#
centres_cantons = {
    "AG": {"lat": 47.40966, "lon": 8.15688},
    "AR": {"lat": 47.366352 + 0.05, "lon": 9.36791},
    "AI": {"lat": 47.317264, "lon": 9.416754},
    "BL": {"lat": 47.45176, "lon": 7.702414},
    "BS": {"lat": 47.564869, "lon": 7.615259},
    "BE": {"lat": 46.823608, "lon": 7.636667},
    "FR": {"lat": 46.718391, "lon": 7.074008},
    "GE": {"lat": 46.220528, "lon": 6.132935},
    "GL": {"lat": 46.981042 - 0.05, "lon": 9.065751},
    "GR": {"lat": 46.656248, "lon": 9.628198},
    "JU": {"lat": 47.350744, "lon": 7.156107},
    "LU": {"lat": 47.067763, "lon": 8.1102},
    "NE": {"lat": 46.995534, "lon": 6.780126},
    "NW": {"lat": 46.926755, "lon": 8.405302},
    "OW": {"lat": 46.854527 - 0.05, "lon": 8.244317 - 0.1},
    "SH": {"lat": 47.71357, "lon": 8.59167},
    "SZ": {"lat": 47.061787, "lon": 8.756585},
    "SO": {"lat": 47.304135, "lon": 7.639388},
    "SG": {"lat": 47.2332 - 0.05, "lon": 9.274744},
    "TI": {"lat": 46.295617, "lon": 8.808924},
    "TG": {"lat": 47.568715, "lon": 9.091957},
    "UR": {"lat": 46.771849, "lon": 8.628586},
    "VD": {"lat": 46.570091, "lon": 6.657809 - 0.1},
    "VS": {"lat": 46.209567, "lon": 7.604659},
    "ZG": {"lat": 47.157296, "lon": 8.537294},
    "ZH": {"lat": 47.41275,  "lon": 8.65508},
    "FL": {"lat": 47.166667, "lon": 9.509722}
}

# 
# Utilities
#
def data_folder():
    return os.path.dirname(__file__)  + "/data"

def output_folder():
    return os.path.dirname(__file__)  + "/output"

#
# Transform
#
def transform_row_openZH_data(row):
    new_row = {}
    # Mapfrom   date,time,abbreviation_canton_and_fl,ncumul_tested,ncumul_conf,ncumul_hosp,ncumul_ICU,ncumul_vent,ncumul_released,ncumul_deceased,source
    # to        date,country,abbreviation_canton,name_canton,lat,long,hospitalized_with_symptoms,intensive_care,total_hospitalized,home_confinment,total_currently_positive_cases,new_positive_cases,recovered,deaths,total_positive_cases,tests_performed

    # Deal with inconsistent date time formats
    try:
        date_time_obj = datetime.datetime.strptime(row['date'], '%d.%m.%Y')
    except:
        date_time_obj = datetime.datetime.strptime(row['date'], '%Y-%m-%d')

    new_row['date'] = date_time_obj
    new_row['country'] = 'CH'
    canton = row['abbreviation_canton_and_fl']
    new_row['abbreviation_canton'] = row['abbreviation_canton_and_fl']
    new_row['name_canton'] = ''
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

#
# Download 
#
def download_file_to_data_folder(url, folder):
    filename = url[url.rfind("/")+1:]
    data_folder = folder
    Path(data_folder).mkdir(parents=True, exist_ok=True)
    target_path = os.path.join(data_folder, filename)
    print("Downloading %s to %s" % (url, target_path) )
    urllib.request.urlretrieve(url, target_path)
    return target_path

def download_openZH_data():
    csv_path_list = []
    for canton in centres_cantons:
        try:
            if canton != 'FL':
                filename = openZH_per_canton_format % canton
            else:
                filename = openZH_per_country_format % canton

            file_path = download_file_to_data_folder(openZH_base_url + filename, os.path.dirname(__file__)  + "/data")
            csv_path_list.append(file_path)
        except:
            # no data
            print("No data for %s" % canton)
        
    return csv_path_list

def download_daenuprobst_data():
    file_path = download_file_to_data_folder(daenuprobst_csv_url, os.path.dirname(__file__)  + "/probst")

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

#
# Main
#
if __name__ == '__main__':
    # Download all data
    download_openZH_data()
    download_daenuprobst_data()
    # Digest data
    table_series = digest_data_total_series(data_folder())
    # Write data to csv files
    time_series_path = os.path.join(output_folder(), "dd-covid19-ch-cantons-series.csv")
    with open(time_series_path, 'w', newline='') as csvfile:        
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(table_series)
