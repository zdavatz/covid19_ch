![Digest OpenZH Data into CSV files](https://github.com/ddrobotec/covid19_ch/workflows/Digest%20OpenZH%20Data%20into%20CSV%20files/badge.svg)
# About
Am 12. März 2020 stellt [@skepteis](https://twitter.com/skepteis/status/1238085013071069185?s=20) die vom BAG Bulletin abgeschriebenen Daten in sein Github Verzeichnis.

Am 20. März 2020 geht das Esri Dashboard von [ddrobotec](http://covid19.ddrobotec.com/) live. [ddrobotec](https://ddrobotec.com/en/) erhält commit Rechte.

Am Wochenende vom 22./23. März 2020 ändert [OpenZH](https://github.com/openZH/covid_19/) seine Datenstrukur und beginnt Daten von den kantonalen Websites gezielt zu sammlen.

Am Montag morgen um 08.00 Uhr am 23. März 2020 geht die [HIN-Email](https://www.hin.ch/covid-19-faelle-ans-bag-melden/) vom BAG online.

Am 25. März 2020 publiziert das BAG zum ersten mal eine [XLSX Datei](https://www.bag.admin.ch/dam/bag/de/dokumente/mt/k-und-i/aktuelle-ausbrueche-pandemien/2019-nCoV/covid-19-datengrundlage-lagebericht.xlsx.download.xlsx/200325_Datengrundlage_Grafiken_COVID-19-Bericht.xlsx) mit seinen offiziellen Zahlen.

Am 26. März 2020 nochmals ein [Blick Artikel](https://www.blick.ch/news/schweiz/wegen-schweizer-corona-karte-berner-programmierer-erntet-lob-bag-unter-beschuss-id15814380.html) zur Daten-Sammlungsweise vom BAG.

Am 27. März 2020 Artikel von Adrienne Fichter in der [Republik](https://www.republik.ch/2020/03/27/bald-ausgefaxt-bag-modernisiert-prozesse-fuer-datenerhebung) zum Thema "Bald ausgefaxt? BAG modernisiert Prozesse für Datenerhebung".

## Data Structures

### Data per Canton

### Data for Switzerland


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
* [Schweiz](https://experience.arcgis.com/experience/115cd04485904fa7a5629b683a949390)
* [JohnHopkins](https://gisanddata.maps.arcgis.com/apps/opsdashboard/index.html#/bda7594740fd40299423467b48e9ecf6)
* [Italy](http://opendatadpc.maps.arcgis.com/apps/opsdashboard/index.html#/b0c68bce2cce478eaac82fe38d4138b1)
* [UK](https://www.arcgis.com/apps/opsdashboard/index.html#/f94c3c90da5b4e9f9a0b19484dd4bb14)
* [Deutschland](https://experience.arcgis.com/experience/478220a4c454480e823b17327b2bf1d4)
* [Frankreich](https://mapthenews.maps.arcgis.com/apps/opsdashboard/index.html#/5e09dff7cb434fb194e22261689e2887)

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
