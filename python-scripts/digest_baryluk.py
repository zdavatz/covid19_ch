import os
import datetime
import pandas as pd

from common_data import *

def download_baryluk_data():
    functor_xyz = pd.read_csv("https://www.functor.xyz/covid_19/scrapers/outputs/latest.txt", sep='\s+', engine='python', keep_default_na=True, header=None).fillna()
    return functor_xyz

def process_baryluk_data(table):
    df = pd.DataFrame(table)
    print(df.shape)

if __name__ == '__main__':
    table = download_baryluk_data()
    process_baryluk_data(table)