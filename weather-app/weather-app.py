import requests
from config import WEATHER_API_KEY

user_input = input("Enter City: ")

weather_data = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={user_input}&units=imperial&APPID={WEATHER_API_KEY}")

# print(weather_data.json())


if weather_data.status_code == 404:
    print("No City Found")
else:
    weather = weather_data.json()['weather'][0]['main']
    temperature = weather_data.json()['main']['temp']

    print(f"{user_input} weather is {weather} and temperature is {temperature} degree celcius")

# lon = weather_data.json()['coord']['lon']
# lat = weather_data.json()['coord']['lat']