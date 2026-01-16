class Weather:
    def __init__(self, city, condition, temp, feels_like, humidity, wind):
        self.city = city
        self.condition = condition
        self.temp = int(temp)
        self.feels_like = feels_like
        self.humidity = humidity
        self.wind = wind

    def icon(self) -> str:
        if "sun" in self.condition or "clear" in self.condition:
            return "☀️"
        if "cloud" in self.condition:
            return "☁️"
        if "rain" in self.condition or "drizzle" in self.condition:
            return "🌧️"
        if "snow" in self.condition:
            return "❄️"
        if "thunder" in self.condition:
            return "⛈️"
        if "fog" in self.condition or "mist" in self.condition:
            return "🌫️"
        return "🌡️"

    def temperature_level(self) -> str:
        if self.temp <= 0:
            return "freezing"
        if self.temp <= 10:
            return "cold"
        if self.temp <= 20:
            return "mild"
        return "hot"
