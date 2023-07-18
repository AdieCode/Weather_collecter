import requests
import pandas as pd
from datetime import datetime
import time


def getWeatherData(api_key, city):
    #description
    """
    function accepts (api_key, city) to access the open weather api and get 
    the city's weather data and returns the data as a dictionary

    @recieve (api_key <-- String, city <-- String)
    @return  (data --> Dictionary)
    """

    #sample of given data
    """
    weather  :  [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}]
    base  :  stations
    main  :  {'temp': 282.43, 'feels_like': 282.43, 'temp_min': 279.09, 'temp_max': 284.21, 'pressure': 1029, 'humidity': 56}
    visibility  :  10000
    wind  :  {'speed': 0.45, 'deg': 135, 'gust': 0.45}
    clouds  :  {'all': 0}
    dt  :  1689538081
    sys  :  {'type': 2, 'id': 2005686, 'country': 'ZA', 'sunrise': 1689483247, 'sunset': 1689521588}
    timezone  :  7200
    id  :  993800
    name  :  Johannesburg
    cod  :  200
    """

    # Make the API request
    try:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
        response = requests.get(url)

        #convert form Json to a python Object
        data = response.json()

        #add time data was extracted
        data["time"] = datetime.now().time()
        return data
    
    #error handeling
    except requests.exceptions.RequestException as e:
    # Handle connection errors, timeouts, or other request-related exceptions
        print("Request error:", e)

    except requests.exceptions.HTTPError as e:
        # Handle HTTP error responses (status codes 4xx or 5xx)
        print("HTTP error occurred:", e)


def getCO2Data(api_key, lat, lon):
    #description
    """
    function accepts (api_key, city) to access the open weather api and get 
    the city's CO2 data and returns the data as a dictionary

    @recieve (api_key <-- String, city <-- String)
    @return  (data --> Dictionary)
    """

    # Make the API request
    try:
        #make API request
        url = f'http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}'
        response = requests.get(url)

        #convert form Json to a python Object
        data = response.json()

        return data
    
    #error handeling
    except requests.exceptions.RequestException as e:
    # Handle connection errors, timeouts, or other request-related exceptions
        print("Request error:", e)

    except requests.exceptions.HTTPError as e:
        # Handle HTTP error responses (status codes 4xx or 5xx)
        print("HTTP error occurred:", e)


def addDataToCsv(data,csv_file):
    """
    Add's the data given to a csv file
    requirements
    ~ data must be a dictionary object
    ~ data must not be empty

    @recieve (data <-- Dictionary, csv_file <-- String)
    @return  (None)
    """
    df = None
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        df = pd.DataFrame()
    except pd.errors.EmptyDataError:
        df = pd.DataFrame()
    except:
        with open(csv_file,"w") as file:
            pass
        df = pd.DataFrame()

    new_data = pd.DataFrame()

    for key, value in data.items():
        new_data[key] = [value]

    df = df._append(pd.DataFrame(new_data), ignore_index=True)
    df.to_csv(csv_file,index=False)



def DisplayWeatherData(data):
    """
    recieves weather data and displays it to the user in
    readable format.

    @recieve (data <-- Dictionary)
    @return  (None)
    """
    try :
        city = data["name"]
        temperature = round(int(data['main']['temp']) - 273.15)
        humidity = data['main']['humidity']
        weather_description = data['weather'][0]['description']
        time  = data['time']
        print(f'City: {city} ')
        print(f'Temperature: {temperature} °C')
        print(f'Humidity: {humidity}%')
        print(f'Weather Description: {weather_description}')
        print(f"Time : {time}")
        print("")
    except:
        print('Error occurred while displaying weather data.')



file = open("secret.txt","r")
api_key = file.read()

citys = ["Pretoria","Johannesburg","Centurion","Midrand","Sandton"]

while True:
    for city in citys:
        try:
            weather_data = getWeatherData(api_key,city)
            co2_data = getCO2Data(api_key,weather_data["coord"]["lat"],weather_data["coord"]["lon"])
            #addDataToCsv(weather_data,"Data/weather_data_raw.csv")
            addDataToCsv(co2_data,"Data/pollution_data_raw.csv")
            DisplayWeatherData(weather_data)
        except:
            print("error occurred while extracting the data")

    time.sleep(600)

