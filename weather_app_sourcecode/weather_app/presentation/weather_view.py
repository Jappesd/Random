from weather_app.presentation.colors import Colors


class WeatherView:
    def __init__(self, use_color: bool = True):
        self.use_color = use_color

    def display(self, weather):

        if self.use_color:
            color = Colors.for_temperature(weather.temperature_level())
            reset = Colors.RESET
        else:
            color = ""
            reset = ""
        print(
            f"""
┌─────────────────────────────┐
│   {weather.icon()}   WEATHER REPORT       │
├─────────────────────────────┤
│ City: {weather.city}
│ Condition: {weather.condition}
│ Temperature: {color}{weather.temp}°C{reset}
│ Feels like: {weather.feels_like}°C
│ Humidity: {weather.humidity}%
│ Wind: {weather.wind} km/h
└─────────────────────────────┘
"""
        )
