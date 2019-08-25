import requests
'''
-only is able to get information for know places with the exception of washington dc (it is refered as district of columbia in the api)
-Maybe convert the place into zip codes and have it gather the information that way

'''
def get_weather(weather_info, city_name):
    weather_api_address = 'http://api.openweathermap.org/data/2.5/weather?appid=dc05695b2edcfce26f852629be3bb618&q='
    city_name = city_name
    url = weather_api_address + city_name
    json_data = requests.get(url).json()
    weather_description = json_data['weather'][0]['description']
    temperature_kelvin = json_data['main']['temp']
    current_temperature = round(temperature_kelvin* (9 / 5) - 459.67)
    max_temperature = json_data['main']['temp_max']
    min_temperature = json_data['main']['temp_min']
    pressure = json_data['main']['pressure']
    humidity = json_data['main']['humidity']
    wind_speed = json_data['wind']['speed'] *2.2369
    wind_direction = json_data['wind']['deg']  # maybe use this as a visual in the GUI?


    if(weather_info == "weather"):
        return "it's "+ weather_description +" with a temperature of "+ str(current_temperature) + " degrees fahrenheit"
    if (weather_info == "temperature"):
        return "the temperature is " + str(current_temperature) + " degrees fahrenheit"
    if(weather_info == "max temperature"):
        return "the max temperature is " + str(max_temperature) + " degrees fahrenheit"
    if(weather_info == "lowest temperature"):
        return "the lowest temperature is " + str(min_temperature) + " degrees fahrenheit"
    if(weather_info == "pressure"):
        return "the pressure is " + str(pressure)
    if(weather_info == "humidity"):
        return "the humidity is " + str(humidity)
    if(weather_info == "wind speed"):
        return "the wind speed is " + str(round(wind_speed)) + " mph"
    if (weather_info == "wind direction"):
        if (-12 < wind_direction < 33):  # Get a general compass direction (may not be completely accurate)
            compass_direction = "north"
            return "the wind direction is " + str(wind_direction) + " degrees, which is moving towards the " + compass_direction + " direction"
        elif (33 < wind_direction < 56):
            compass_direction = "north east"
            return "the wind direction is " + str(wind_direction) + " degrees, which is moving towards the " + compass_direction + " direction"
        elif (56 < wind_direction < 101):
            compass_direction = "east"
            return "the wind direction is " + str(wind_direction) + " degrees, which is moving towards the " + compass_direction + " direction"
        elif (101 < wind_direction < 146):
            compass_direction = "south east"
            return "the wind direction is " + str(wind_direction) + " degrees, which is moving towards the " + compass_direction + " direction"
        elif (146 < wind_direction < 191):
            compass_direction = "south"
            return "the wind direction is " + str(wind_direction) + " degrees, which is moving towards the " + compass_direction + " direction"
        elif (191 < wind_direction < 236):
            compass_direction = "south west"
            return "the wind direction is " + str(wind_direction) + " degrees, which is moving towards the " + compass_direction + " direction"
        elif (236 < wind_direction < 281):
            compass_direction = "west"
            return "the wind direction is " + str(wind_direction) + " degrees, which is moving towards the " + compass_direction + " direction"
        elif (281 < wind_direction < 348):
            compass_direction = "north west"
            return "the wind direction is " + str(wind_direction) + " degrees, which is moving towards the " + compass_direction + " direction"
