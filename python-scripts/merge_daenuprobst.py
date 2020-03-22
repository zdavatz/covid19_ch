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

def merge_daenuprobst_switzerland_files():
    positive_cases = pd.read_csv("https://raw.githubusercontent.com/daenuprobst/covid19-cases-switzerland/master/covid19_cases_switzerland.csv")

    fatalities = pd.read_csv("https://raw.githubusercontent.com/daenuprobst/covid19-cases-switzerland/master/covid19_fatalities_switzerland.csv")
    fatalities = fatalities.drop(['CH'], axis=1)
    fatalities = fatalities.fillna(method='ffill')
    fatalities['deaths'] = fatalities.sum(axis=1).astype('int32')

    print(fatalities)

    # date,country,hospitalized_with_symptoms,intensive_care,total_hospitalized,home_confinment,total_currently_positive,new_positive,recovered,deaths,total_positive,tests_performed

    switzerland_latest = pd.concat([fatalities['Date']], axis=1)
    switzerland_latest = switzerland_latest.rename(columns={"Date": "date"})
    # Add columns
    switzerland_latest['country'] = 'CH'
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

def merge_daenuprobst_canton_files():
    positive_cases = pd.read_csv("https://raw.githubusercontent.com/daenuprobst/covid19-cases-switzerland/master/covid19_cases_switzerland.csv", index_col=[0])
    positive_cases = positive_cases.fillna(method='ffill')
    # Extract last row and transpose (ignore Switzerland, last row)
    latest_cases = positive_cases.iloc[-1,:-1]
    date = latest_cases.name
    # name column
    latest_cases.name = 'total_currently_positive_cases'
    # create dataframe
    df = pd.DataFrame(latest_cases)
    # rename index
    df.index.name = 'abbreviation_canton'
    # drop switzerland
    print(df)

    cantons_col = df.index

    df.insert(0, 'date', date)
    df.insert(1, 'country', 'CH')
    df.insert(2, 'abbreviation_canton', cantons_col)
    df.insert(3, 'name_canton', list(map(lambda name: name_and_numbers_cantons[name]['name'], cantons_col)))
    df.insert(4, 'number_canton', list(map(lambda name: name_and_numbers_cantons[name]['number'], cantons_col)))
    df.insert(5, 'lat', list(map(lambda name: centres_cantons[name]['lat'], cantons_col )))
    df.insert(6, 'long', list(map(lambda name: centres_cantons[name]['lon'], cantons_col )))
    df.insert(7, 'tests_performed', 0)
    df['total_currently_positive_cases'] = df['total_currently_positive_cases'].astype('Int64')
    df['total_positive_cases'] = df['total_currently_positive_cases']
    df['new_positive_cases'] = 0
    df['home_confinment'] = 0
    df['total_hospitalized'] = 0
    df['hospitalized_with_symptoms'] = 0
    df['intensive_care'] = 0
    df['recovered'] = 0
    df['deaths'] = 0

    print(df)

    file_name = output_folder() + "../../../data-cantons-csv/dd-covid19-ch-cantons-latest.csv"
    df.to_csv(file_name, mode="w", index=False)


if __name__ == '__main__':
    merge_daenuprobst_switzerland_files()
    merge_daenuprobst_canton_files()