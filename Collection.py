
from api_authentication import *
from station_helper import *
import pandas as pd
from timetable_helper import *
from datetime import datetime
import subprocess

# Authenticate API
api = ApiAuthentication("bef6017966eb3a7883800d136b0e8de4", "a7dfa9a925d50c6b8cb226cd3405b2f3")
success: bool = api.test_credentials()

# Find stations
station_helper = StationHelper()
found_stations_by_name = station_helper.find_stations_by_name("Erlangen")
found_stations_by_name = pd.DataFrame(found_stations_by_name)

# Define Station details
station = Station(
    EVA_NR=8001844,
    DS100="NER",
    IFOPT="de:09562:3110",  
    NAME="Erlangen",  
    Verkehr="FV",         
    Laenge="11,0016382",       
    Breite="49,5958303",      
    Betreiber_Name="DB Station und Service AG",  
    Betreiber_Nr=1650,    
    Status="active"       
)

# Get timetable data
timetable_helper = TimetableHelper(station, api)
data_list = []

# Planned timetable

for j in range(23):
    trains_at_given_hour = timetable_helper.get_timetable(j)
    for train in trains_at_given_hour:
        data = {
            'Hour': j,
            'Stop_id': getattr(train, 'stop_id', 'null'),
            'Trip_type': getattr(train, 'trip_type', 'null'),
            'Train_Type': getattr(train, 'train_type', 'null'),
            'Train_number': getattr(train, 'train_number', 'null'),
            'Platform': getattr(train, 'platform', 'null'),
            'Passed_Stations': getattr(train, 'passed_stations', 'null'),
            'Stations': getattr(train, 'stations', 'null'),
            'Arrival': getattr(train, 'arrival', 'null'),
            'Departure': getattr(train, 'departure', 'null')
        }
        data_list.append(data)

# Create and save DataFrame
df = pd.DataFrame(data_list)
csv_file = 'train_timetable_23.csv'
df.to_csv(csv_file, index=False)

