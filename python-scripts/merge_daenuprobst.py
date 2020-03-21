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

def output_folder():
    return os.path.dirname(os.path.abspath(__file__))  + "/output"

def merge_daenuprobst_files():
    positive_cases = pd.read_csv("https://raw.githubusercontent.com/daenuprobst/covid19-cases-switzerland/master/covid19_cases_switzerland.csv")

    fatalities = pd.read_csv("https://raw.githubusercontent.com/daenuprobst/covid19-cases-switzerland/master/covid19_fatalities_switzerland.csv")    
    fatalities = fatalities.drop(['CH'], axis=1)
    fatalities['deaths'] = fatalities.sum(axis=1).astype('int32')

    # date,country,hospitalized_with_symptoms,intensive_care,total_hospitalized,home_confinment,total_currently_positive,new_positive,recovered,deaths,total_positive,tests_performed

    switzerland_latest = pd.concat([fatalities['Date']], axis=1)
    switzerland_latest = switzerland_latest.rename(columns={"Date": "date"})
    # Add columns
    switzerland_latest['tests_performed'] = 0
    switzerland_latest['total_currently_positive'] = positive_cases['CH']
    switzerland_latest['total_positive'] = positive_cases['CH']
    switzerland_latest['new_positive'] = positive_cases['CH'].diff(periods=1).astype('Int64')
    switzerland_latest['home_confinment'] = 0
    switzerland_latest['total_hospitalized'] = 0
    switzerland_latest['hospitalized_with_symptoms'] = 0
    switzerland_latest['intensive_care'] = 0
    switzerland_latest['recovered'] = 0
    switzerland_latest['deaths'] = fatalities['deaths']

    file_name = output_folder() + "../../../data-switzerland-csv/dd-covid19-ch-switzerland-latest.csv"
    switzerland_latest.to_csv(file_name, mode="w", index=False)

if __name__ == '__main__':
    merge_daenuprobst_files()