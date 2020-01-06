import pandas as pd

# MAPBOX PUBLIC KEY
mapbox_publictoken = "pk.eyJ1IjoiYmVya2FrdHVnIiwiYSI6ImNrNTF4ZmxoZzAyMWkza3FlaHlleGRlczEifQ.V8xoVT7aufNvLudx9eDdUA"

# DATABASE
DATABASE_NAME = "TlcDB.db"
TABLE_NAME = 'tripdata'

df = pd.read_csv("yellow_tripdata_2017-04.csv")

df["tpep_pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"], format = "%Y-%m-%d %H:%M:%S")
date_series = df["tpep_pickup_datetime"].dt.date
min_date = date_series.min()
max_date = date_series.max()

# LOCATION
locationDataframe = pd.read_csv("taxi_zones.csv")
locationList = {value: {"lat": locationDataframe['Y'][index], "lon": locationDataframe['X'][index]}
                     for index, value in enumerate(locationDataframe['zone'])}
locationDictionary = {locationDataframe['zone'][index]: locationDataframe['LocationID'][index] for index, _ in enumerate(locationDataframe['zone'])}
