## Data Formats

### Data per Canton

**Directory:**  [data-cantons-csv](https://github.com/zdavatz/covid19_ch/tree/master/data-cantons-csv)<br>
**Structure daily file:** dd-covid19-ch-cantons-yyyymmdd.csv see sample file [dd-covid19-ch-cantons-20200318.csv](https://github.com/zdavatz/covid19_ch/blob/master/data-cantons-csv/dd-covid19-ch-cantons-20200318-example.csv)<br>
**File most recent data (latest):** [dd-covid19-ch-cantons-latest.csv](https://github.com/zdavatz/covid19_ch/blob/master/data-cantons-csv/dd-covid19-ch-cantons-latest.csv)<br>

| Field Name                              | Description                            | Description                                 | Format              | Example             |
|-----------------------------------------|----------------------------------------|---------------------------------------------|---------------------|---------------------|
| **date**                                | Date of notification                   | YYYY-MM-DD HH:MM:SS (ISO 8601) Swiss time   | 2020-03-05 12:15:45 |
| **country**                             | Country of reference                   | XY (ISO 3166-1 alpha-2)                     | CH                  |
| **abbreviation_canton**                 | Abbreviation of canton                 | XY (ISO 3166-1 alpha-2)                     | ZH                  |
| **name_canton**                         | Name of the canton                     | Text                                        | Zurich              |
| **lat**                                 | Latitude                               | WGS84                                       | 42.6589177          |
| **long**                                | Longitude                              | WGS84                                       | 13.70439971         |
| **hospitalized_with_symptoms**          | Hospitalised patients with symptoms    | Number                                      | 3                   |
| **intensive_care**                      | Intensive care                         | Number                                      | 3                   |
| **total_hospitalized**                  | Total hospitalised patients            | Number                                      | 3                   |
| **home_confinment**                     | Home confinement                       | Number                                      | 3                   |
| **total_currently_positive_cases**      | Total amount of current positive cases (Hospitalised patients + Home confinement)    | Number              | 3                   |
| **new_positive_cases**                  | News amount of current positive cases (Actual total amount of current positive cases - total amount of current positive cases of the previous day)  | Number                        | 3                   |
| **recovered**                           | Recovered                              | Number                                      | 3                   |
| **deaths**                              | Death                                  | Number                                      | 3                   |
| **total_positive_cases**                | Total amount of positive cases         | Number                                      | 3                   |
| **tests_performed**                     | Tests performed                        | Number                                      | 3                   |


### Data for Switzerland

**Directory:**  [data-switzerland-csv](https://github.com/zdavatz/covid19_ch/tree/master/data-switzerland-csv)<br>
**Structure daily file:** dd-covid19-ch-switzerland-yyyymmdd.csv see the sample file [dd-covid19-ch-switzerland-20200318.csv](https://github.com/zdavatz/covid19_ch/blob/master/data-switzerland-csv/dd-covid19-ch-switzerland-20200318-example.csv)<br>
**File most recent data (latest):** [dd-covid19-ch-switzerland-latest.csv](https://github.com/zdavatz/covid19_ch/blob/master/data-switzerland-csv/dd-covid19-ch-switzerland-latest.csv)<br>

| Field Name                            | Description                            | Format                                    | Example             |
|---------------------------------------|----------------------------------------|-------------------------------------------|---------------------|
| **date**                              | Date of notification                   | YYYY-MM-DD HH:MM:SS (ISO 8601) Swiss time | 2020-03-05 12:15:45 |
| **country**                           | Country of reference                   | XYZ (ISO 3166-1 alpha-2)                  | CH                  |
| **hospitalized_with_symptoms**        | Hospitalised patients with symptoms    | Number                                    | 3                   |
| **intensive_care**                    | Intensive care                         | Number                                    | 3                   |
| **total_hospitalized**                | Total hospitalised patients            | Number                                    | 3                   |
| **home_confinment**                   | Home confinement                       | Number                                    | 3                   |
| **total_currently_positive_cases**    | Total amount of current positive cases (Hospitalised patients + Home confinement)  | Number              | 3                   |
| **new_positive_cases**                | News amount of current positive cases (Hospitalised patients + Home confinement)   | Number              | 3                   |
| **recoverd**                          | Recovered                              | Number                                    | 3                   |
| **deaths**                            | Death                                  | Number                                    | 3                   |
| **total_positive_cases**              | Total amount of positive cases         | Number                                    | 3                   |
| **tests_performed**                   | Tests performed                        | Number                                    | 3                   |


# Landkarte der Schweiz für die Covid19 Fälle
* [Desktop Version](https://ddrobotec.maps.arcgis.com/apps/opsdashboard/index.html#/5ed2e108dbab4235a7318d1cfe147e7a)
* [Mobile Version](https://ddrobotec.maps.arcgis.com/apps/opsdashboard/index.html#/3fa74da8e6c74229af19661eb7fa97d2)

## Esri Visualisierungen
* [Schweiz-1](http://covid19.ddrobotec.com)
* [Schweiz-2](https://ddrobotec.maps.arcgis.com/apps/opsdashboard/index.html#/5ed2e108dbab4235a7318d1cfe147e7a)
* [JohnHopkins](https://gisanddata.maps.arcgis.com/apps/opsdashboard/index.html#/bda7594740fd40299423467b48e9ecf6)
* [Italy](http://opendatadpc.maps.arcgis.com/apps/opsdashboard/index.html#/b0c68bce2cce478eaac82fe38d4138b1)
* [UK](https://www.arcgis.com/apps/opsdashboard/index.html#/f94c3c90da5b4e9f9a0b19484dd4bb14)
* [Deutschland](https://experience.arcgis.com/experience/478220a4c454480e823b17327b2bf1d4)

## Todesfälle in der Schweiz
* [Wikipedia](https://de.wikipedia.org/wiki/COVID-19-Pandemie_in_der_Schweiz#Todesf%C3%A4lle)

## Daten manuell gesammelt
* [Dänu Probst](https://github.com/daenuprobst/covid19-cases-switzerland)

## Hochrechnungen
* https://neherlab.org/covid19/
* http://gabgoh.github.io/COVID/index.html by https://twitter.com/gabeeegoooh
