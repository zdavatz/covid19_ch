
field_names = "date,country,abbreviation_canton,name_canton,number_canton,lat,long,hospitalized_with_symptoms,intensive_care,total_hospitalized,home_confinment,total_currently_positive_cases,new_positive_cases,recovered,deaths,total_positive_cases,tests_performed".split(',')
field_names_short = "date,country,hospitalized_with_symptoms,intensive_care,total_hospitalized,home_confinment,total_currently_positive,new_positive,recovered,deaths,total_positive,tests_performed".split(',')

# Direct field mappings to our format
openzh_field_mapping = {
    "date" : "date",
    "abbreviation_canton_and_fl" : "abbreviation_canton",
    "ncumul_tested" : "tests_performed",
    "ncumul_conf" : "total_positive_cases",
    "ncumul_hosp" : "total_hospitalized",
    "ncumul_ICU" : "intensive_care",
    "ncumul_vent" : "ncumul_vent",
    "ncumul_released" : "ncumul_released",
    "ncumul_deceased" : "deaths",
    "source" : "source",
    "TotalPosTests1" : "pos_tests_1",
    "TotalCured" : "recovered"
}

# Data Sources

# Latest data per canton and for Switzerland
# Using data provided by OpenZH: Statistische Amt, Kanton Zuerich on Github
# https://github.com/openZH/covid_19

openZH_base_url = 'https://raw.githubusercontent.com/openZH/covid_19/master/fallzahlen_kanton_total_csv/'
openZH_per_canton_format = 'COVID19_Fallzahlen_Kanton_%s_total.csv'
openZH_per_country_format = 'COVID19_Fallzahlen_%s_total.csv'

# Latest data per canton 
# https://github.com/daenuprobst/covid19-cases-switzerland
daenuprobst_csv_url = "https://raw.githubusercontent.com/daenuprobst/covid19-cases-switzerland/master/covid19_cases_switzerland.csv"

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

name_and_numbers_cantons = {
    "AG": {"name": "Aargau", "number": "01"},
    "AR": {"name": "Appenzell Ausserrhoden", "number": "15"},
    "AI": {"name": "Appenzell Innerrhoden", "number": "16"},
    "BL": {"name": "Basel-Landschaft", "number": "13"},
    "BS": {"name": "Basel-Stadt", "number": "12"},
    "BE": {"name": "Bern", "number": "02"},
    "FR": {"name": "Fribourg", "number": "10"},
    "GE": {"name": "Genève", "number": "25"},
    "GL": {"name": "Glarus", "number": "08"},
    "GR": {"name": "Graubünden", "number": "01"},
    "JU": {"name": "Jura", "number": "26"},
    "LU": {"name": "Luzern", "number": "03"},
    "NE": {"name": "Neuchatel", "number": "24"},
    "NW": {"name": "Nidwalden", "number": "07"},
    "OW": {"name": "Obwalden", "number": "06"},
    "SH": {"name": "Schaffhausen", "number": "14"},
    "SZ": {"name": "Schwyz", "number": "05"},
    "SO": {"name": "Solothurn", "number": "11"},
    "SG": {"name": "St. Gallen", "number": "17"},
    "TI": {"name": "Ticino", "number": "21"},
    "TG": {"name": "Thurgau", "number": "01"},
    "UR": {"name": "Uri", "number": "04"},
    "VD": {"name": "Vaud", "number": "22"},
    "VS": {"name": "Valais", "number": "23"},
    "ZG": {"name": "Zug", "number": "09"},
    "ZH": {"name": "Zürich", "number": "01"},
    "FL": {"name": "Fürstentum Lichtenstein", "number": "00"}
}
