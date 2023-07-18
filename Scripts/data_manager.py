import pandas as pd
import datetime
import pytz
import json

def fixJson(row,column):
    # Fix JSON string by replacing single quotes with double quotes
    fixed_json = row[column].replace("'", '"')

    return fixed_json




def convert_unix_to_utc(unix_time, timezone_offset):
    # Convert Unix time to a datetime object
    utc_datetime = datetime.datetime.utcfromtimestamp(unix_time)

    # Create a UTC timezone object
    utc_timezone = pytz.timezone('UTC')

    # Apply the time zone offset to the datetime object
    localized_datetime = utc_timezone.localize(utc_datetime) + datetime.timedelta(seconds=timezone_offset)

    # Convert datetime object to a string in UTC format
    utc_time = localized_datetime.strftime('%Y-%m-%d %H:%M:%S UTC')

    return utc_time



def CleanWeatherDataframe(df):
    """
    function that will create a whole new clean dataframe
    """
    new_df = pd.DataFrame()


    # Iterate over the rows
    for index, row in df.iterrows():

        # Parse the JSON string in the "weather" column
        weather_data = json.loads(fixJson(row,"weather"))
        main_data = json.loads(fixJson(row, "main"))
        wind_data = json.loads(fixJson(row, "wind"))
        clouds_data = json.loads(fixJson(row, "clouds"))
        sys_data = json.loads(fixJson(row, "sys"))


        # Extract the "description" field and assign it to a new column
        new_row = {"description": weather_data[0]["description"],
                   "temp" : main_data["temp"],
                   "feels_like" : main_data["feels_like"],
                   "temp_min" : main_data["temp_min"],
                   "temp_max" : main_data["temp_max"],
                   "pressure" : main_data["pressure"],
                   "humidity" : main_data["humidity"],
                   "visibility" : row["visibility"],
                   "wind_speed" : wind_data["speed"],
                   "wind_deg" : wind_data["deg"],
                   "clouds" : clouds_data["all"],
                   "date" : convert_unix_to_utc(row["dt"],row["timezone"]),
                   "country" : sys_data["country"],
                   "city" : row["name"],}
        
        new_df = new_df._append(new_row, ignore_index=True)


    new_df.to_csv("Data/weather.csv",index=False)



def CleanCO2Dataframe(df):
    """
    function that will create a whole new clean dataframe
    """
    new_df = pd.DataFrame()


    # Iterate over the rows
    for index, row in df.iterrows():

        # Parse the JSON string in the "weather" column
        list_data = json.loads(fixJson(row, "list"))
        coord_data = json.loads(fixJson(row,"coord"))

        # Extract the "description" field and assign it to a new column
        new_row = {"aqi": list_data[0]["main"]["aqi"],
                   "no" : list_data[0]["components"]['no'],
                   "no2" : list_data[0]["components"]['no2'],
                   "o3" : list_data[0]["components"]['o3'],
                   "so2" : list_data[0]["components"]['so2'],
                   "pm2_5" : list_data[0]["components"]['pm2_5'],
                   "pm10" : list_data[0]["components"]['pm10'],
                   "nh3" : list_data[0]["components"]['nh3'],
                   "date" :  convert_unix_to_utc(list_data[0]["dt"],7200),
                   "lat" : coord_data["lat"],
                   "lon" : coord_data["lon"],
                   }
        
        new_df = new_df._append(new_row, ignore_index=True)


    new_df.to_csv("Data/pollution.csv",index=False)


# control 
weather_df = pd.read_csv("Data/weather_data_raw.csv")
co2_df = pd.read_csv("Data/pollution_data_raw.csv")
CleanWeatherDataframe(weather_df)
CleanCO2Dataframe(co2_df)