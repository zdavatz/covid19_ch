![Digest OpenZH Data into CSV files](https://github.com/ddrobotec/covid19_ch/workflows/Digest%20OpenZH%20Data%20into%20CSV%20files/badge.svg)
# About
Am 12. März 2020 stellt [@skepteis](https://twitter.com/skepteis/status/1238085013071069185?s=20) die vom BAG Bulletin abgeschriebenen Daten in sein Github Verzeichnis.

Am 20. März 2020 geht das Esri Dashboard von [ddrobotec](http://covid19.ddrobotec.com/) live. [WeEnterMute](https://github.com/weentermute) erhält commit Rechte.

Am Wochenende vom 22./23. März 2020 ändert [OpenZH](https://github.com/openZH/covid_19/) seine Datenstrukur und beginnt Daten von den kantonalen Websites gezielt zu sammlen.

Am Montag morgen um 08.00 Uhr am 23. März geht die HIN-Email vom BAG online.

Am 25. März 2020 publiziert das BAG zum ersten mal eine [XLSX Datei](https://www.bag.admin.ch/dam/bag/de/dokumente/mt/k-und-i/aktuelle-ausbrueche-pandemien/2019-nCoV/covid-19-datengrundlage-lagebericht.xlsx.download.xlsx/200325_Datengrundlage_Grafiken_COVID-19-Bericht.xlsx) mit seinen offiziellen Zahlen.

## Data Structures

### Data per Canton

**Directory:**  [data-cantons-csv](https://github.com/zdavatz/covid19_ch/tree/master/data-cantons-csv)<br>
**Structure daily file:** dd-covid19-ch-cantons-yyyymmdd.csv see sample file [dd-covid19-ch-cantons-20200318.csv](https://github.com/zdavatz/covid19_ch/blob/master/data-cantons-csv/dd-covid19-ch-cantons-20200318-example.csv)<br>
**File most recent data (latest):** [dd-covid19-ch-cantons-latest.csv](https://github.com/zdavatz/covid19_ch/blob/master/data-cantons-csv/dd-covid19-ch-cantons-latest.csv)<br>

| Field Name                              | Description                            | Format                                      | Example             |
|-----------------------------------------|----------------------------------------|---------------------------------------------|---------------------|
| **date**                                | Date of notification                   | YYYY-MM-DD HH:MM:SS (ISO 8601) Swiss time   | 2020-03-05 12:15:45 |
| **country**                             | Country of reference                   | XY (ISO 3166-1 alpha-2)                     | CH                  |
| **abbreviation_canton**                 | Abbreviation of canton                 | XY (ISO 3166-1 alpha-2)                     | ZH                  |
| **name_canton**                         | Name of the canton                     | Text                                        | Zurich              |
| **number_canton**                       | Number of the canton                   | Number                                      | 10                  |
| **lat**                                 | Latitude                               | WGS84                                       | 42.6589177          |
| **long**                                | Longitude                              | WGS84                                       | 13.70439971         |
| **hospitalized_with_symptoms**          | Hospitalised patients with symptoms    | Number                                      | 3                   |
| **intensive_care**                      | Intensive care                         | Number                                      | 3                   |
| **total_hospitalized**                  | Total hospitalised patients            | Number                                      | 3                   |
| **home_confinment**                     | Home confinement                       | Number                                      | 3                   |
| **total_currently_positive**            | Total amount of current positive cases (Hospitalised patients + Home confinement)    | Number              | 3                   |
| **new_positive**                        | News amount of current positive cases (Actual total amount of current positive cases - total amount of current positive cases of the previous day)  | Number                        | 3                   |
| **recovered**                           | Recovered                              | Number                                      | 3                   |
| **deaths**                              | Death                                  | Number                                      | 3                   |
| **total_positive**                      | Total amount of positive cases         | Number                                      | 3                   |
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
| **total_currently_positives**         | Total amount of current positive cases (Hospitalised patients + Home confinement)  | Number              | 3                   |
| **new_positive**                      | New amount of current positive cases (Hospitalised patients + Home confinement)    | Number              | 3                   |
| **recoverd**                          | Recovered                              | Number                                    | 3                   |
| **deaths**                            | Death                                  | Number                                    | 3                   |
| **total_positive**                    | Total amount of positive cases         | Number                                    | 3                   |
| **tests_performed**                   | Tests performed                        | Number                                    | 3                   |
    

## Data on the measures taken against Covid2019

### Data format
I settled on the current long csv format:


| date_implemented | date_lifted | measure | unit | level |
| -----------------|-------------|----------|------|-------- |
| date when the measure is implemented | date when the measure is lifted | textual description of the measure | identifier of the administrative unit | level of the administrative unit (canton, city, federal) |


### Next steps
- add measures for all cantons and federal and city level measures.
- code them according to general categories (Veranstaltungsverbot, ...) according to Art. 40 of the [Epiemiegesetzt](https://www.admin.ch/opc/de/classified-compilation/20071012/index.html#a40)


# Landkarte der Schweiz für die Covid19 Fälle
* [Desktop Version](https://ddrobotec.maps.arcgis.com/apps/opsdashboard/index.html#/5ed2e108dbab4235a7318d1cfe147e7a)
* [Mobile Version](https://ddrobotec.maps.arcgis.com/apps/opsdashboard/index.html#/3fa74da8e6c74229af19661eb7fa97d2)

## andere Esri Visualisierungen
* [JohnHopkins](https://gisanddata.maps.arcgis.com/apps/opsdashboard/index.html#/bda7594740fd40299423467b48e9ecf6)
* [Italy](http://opendatadpc.maps.arcgis.com/apps/opsdashboard/index.html#/b0c68bce2cce478eaac82fe38d4138b1)
* [UK](https://www.arcgis.com/apps/opsdashboard/index.html#/f94c3c90da5b4e9f9a0b19484dd4bb14)
* [Deutschland](https://experience.arcgis.com/experience/478220a4c454480e823b17327b2bf1d4)

## Todesfälle in der Schweiz
* [Wikipedia](https://de.wikipedia.org/wiki/COVID-19-Pandemie_in_der_Schweiz#Todesf%C3%A4lle)

## Daten manuell gesammelt
* [Dänu Probst](https://github.com/daenuprobst/covid19-cases-switzerland)
* [Daten gesammelt durch das Statistische Amt des Kanton Zürich](https://github.com/openZH/covid_19/#covid-19-cases-communicated-by-swiss-cantons-and-principality-of-liechtenstein-fl)

## Spitäler
* Alle [Spitäler der Schweiz](https://github.com/zdavatz/covid19_ch/blob/master/additional-infos/partner_jur_refdata_21.3.2020.xml) mit GLN Code. Daten sind von [Refdata.ch](https://refdata.ch) und können täglich aktulaisiert werden, falls erwünscht.

## Hochrechnungen
* https://neherlab.org/covid19/
* http://gabgoh.github.io/COVID/index.html by https://twitter.com/gabeeegoooh

## Medienberichte
* [Die Zahl der Todesfälle haben wir aus Wikipedia entnommen](https://www.republik.ch/2020/03/20/die-zahl-der-todesfaelle-haben-wir-aus-wikipedia-entnommen) Republik 20.3.2020
* [Bis ein toter Coronavirus-Patient in der Statistik auftaucht, können über 30 Stunden vergehen](https://www.nzz.ch/schweiz/coronavirus-das-bag-kommt-bei-erfassung-der-faelle-kaum-hinterher-ld.1547359?mktcid=smch&mktcval=twpost_2020-03-20) NZZ 20.3.2020
