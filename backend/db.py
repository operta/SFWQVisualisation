import sqlite3
import csv
import datetime

# Method to transform date format
def transform(date):
    return datetime.datetime.strptime(date.strip(), "%m/%d/%Y").strftime("%Y/%m/%d")


if __name__ == '__main__':
    con = sqlite3.connect(r"pythonsqlite.db")
    cur = con.cursor()

    # Create data table
    cur.execute("CREATE TABLE data (Datum TEXT, StationNumber REAL, Latitude REAL, Longitude REAL, Depth REAL, Fluorescence REAL,"
                " CalculatedChlorophyll REAL, OxygenElectrodeOutput REAL, OxygenSaturation REAL, CalculatedOxygen REAL,"
                " OpticalBackscatter REAL, CalculatedSPM REAL, Salinity REAL, Temperature REAL, SigmaT REAL);")  # use your column names here

    # Open data.csv and insert it into data table
    with open('data.csv') as fin:
        dr = csv.DictReader(fin)
        to_db = [(transform(i['Date']), i['Station Number'], i['lat'], i['long'], i['Depth'], i['Fluorescence'],
                  i['Calculated Chlorophyll'], i['Oxygen Electrode Output'], i['Oxygen Saturation %'],
                  i['Calculated Oxygen'], i['Optical Backscatter'], i['Calculated SPM'], i['Salinity'],
                  i['Temperature'], i['Sigma-t']) for i in dr]

    cur.executemany("INSERT INTO data (Datum, StationNumber, Latitude, Longitude, Depth, Fluorescence,"
                    " CalculatedChlorophyll, OxygenElectrodeOutput, OxygenSaturation, CalculatedOxygen,"
                    " OpticalBackscatter, CalculatedSPM, Salinity, Temperature, SigmaT)"
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", to_db)

    #Create stations table
    cur.execute("CREATE TABLE stations (StationNumber REAL, Latitude REAL, Longitude REAL);")

    # Open sngeo.csv and insert it into stations table
    with open('sngeo.csv') as fin:
        dr = csv.DictReader(fin)
        to_db = [(i['num'], i['latitude'], i['longitude']) for i in dr]

    cur.executemany("INSERT INTO stations (StationNumber, Latitude, Longitude)"
                    "VALUES (?, ?, ?);", to_db)

    con.commit()
    con.close()
