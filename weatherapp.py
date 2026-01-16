import requests

CITY = "Helsinki"

url = f"https://wttr.in/{CITY}?format=j1"
data = requests.get(url).json()

current = data["current_condition"][0]

temp = current["temp_C"]
feels_like = current["FeelsLikeC"]
weather_desc = current["weatherDesc"][0]["value"]
humidity = current["humidity"]
wind = current["windspeedKmph"]

print(
    f"""
┌─────────────────────────────┐
│        WEATHER REPORT       │
├─────────────────────────────┤
│ City: {CITY}                
│ Condition: {weather_desc}    
│ Temperature: {temp}°C         
│ Feels like: {feels_like}°C  
│ Humidity: {humidity}%       
│ Wind: {wind} km/h           
└─────────────────────────────┘
"""
)
