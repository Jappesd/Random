import requests
from weather_app.domain.weather_model import Weather


class WeatherService:
    def fetch_current_weather(self, city: str) -> Weather:
        url = f"https://wttr.in/{city}?format=j1"
        data = requests.get(url).json()

        current = data["current_condition"][0]

        return Weather(
            city=city,
            condition=current["weatherDesc"][0]["value"],
            temp=current["temp_C"],
            feels_like=current["FeelsLikeC"],
            humidity=current["humidity"],
            wind=current["windspeedKmph"],
        )
