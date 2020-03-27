import os
import datetime
import pandas as pd

from common_data import *

def download_baryluk_data():
    functor_xyz = pd.read_csv("http://pillbox.oddb.org/current.txt", sep='\s+', engine='python', error_bad_lines=False, keep_default_na=True, header=None)
    return functor_xyz

def process_baryluk_data(table):
    df = pd.DataFrame(table)
    print(df)
    print(df.shape)

if __name__ == '__main__':
    table = download_baryluk_data()
    process_baryluk_data(table)