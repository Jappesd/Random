import tkinter as tk
from weather_app.services.weather_service import WeatherService
from weather_app.presentation.weather_view import WeatherView

# map temp levels to colors
temp_colors = {
    "freezing": "blue",
    "cold": "cyan",
    "mild": "green",
    "hot": "red",
}
# Map temperature levels to background colors
BG_COLORS = {
    "freezing": "#a0c4ff",  # icy blue
    "cold": "#caf0f8",  # light cyan
    "mild": "#d8f3dc",  # soft green
    "hot": "#ffadad",  # warm red/pink
}


class WeatherGui:
    def __init__(self):
        self.service = WeatherService()
        # root
        self.root = tk.Tk()
        self.root.title("Weather App")
        self.root.geometry("350x300")
        self.root.resizable(False, False)
        # input
        self.city_label = tk.Label(self.root, text="City:")
        self.city_label.pack(pady=5)
        self.city_entry = tk.Entry(self.root)
        self.city_entry.pack(pady=5)
        self.city_entry.insert(0, "Joensuu")  # default city

        # button
        self.get_button = tk.Button(
            self.root, text="Get Weather", command=self.show_weather
        )
        self.get_button.pack(pady=10)
        # output icon and info labels
        self.icon_label = tk.Label(self.root, text="", font=("Courier", 20))
        self.icon_label.pack(pady=5)

        self.info_label = tk.Label(
            self.root, text="", justify="left", font=("Courier", 10)
        )
        self.info_label.pack(pady=5)

        self.root.mainloop()

    def show_weather(self):

        city = self.city_entry.get() or "Joensuu"
        weather = self.service.fetch_current_weather(city)

        # color based on temp
        temp_level = weather.temperature_level()
        temp_color = temp_colors[temp_level]
        # background color
        bg_color = BG_COLORS.get(temp_level, "white")
        # update icon label
        self.icon_label.config(text=weather.icon(), bg=bg_color, fg=temp_color)

        self.root.configure(bg=bg_color)
        # Also update child widgets bg for consistency
        for widget in [
            self.city_label,
            self.city_entry,
            self.get_button,
            self.info_label,
        ]:
            widget.configure(bg=bg_color)
        # Build output text (similar to cli)
        text = f"Weather in {weather.city}\n"
        text += f"Condition: {weather.condition.title()}\n"
        text += f"Temperature: {weather.temp}°C (Feels like {weather.feels_like}°C)\n"
        text += f"Humidity: {weather.humidity}%\n"
        text += f"Wind: {weather.wind} km/h"

        self.info_label.config(text=text)


if __name__ == "__main__":
    WeatherGui()
