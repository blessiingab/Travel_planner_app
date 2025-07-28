import tkinter as tk
from tkinter import messagebox
import requests  # Added for API calls

class TravelPlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Travel Planner App")
        self.root.geometry("350x350")  # Set a smaller window size

        # Input fields
        tk.Label(root, text="Destination:").grid(row=0, column=0, sticky="e")
        self.destination_entry = tk.Entry(root, width=20)
        self.destination_entry.grid(row=0, column=1)

        tk.Label(root, text="Start Date:").grid(row=1, column=0, sticky="e")
        self.start_date_entry = tk.Entry(root, width=20)
        self.start_date_entry.grid(row=1, column=1)

        tk.Label(root, text="End Date:").grid(row=2, column=0, sticky="e")
        self.end_date_entry = tk.Entry(root, width=20)
        self.end_date_entry.grid(row=2, column=1)

        tk.Label(root, text="Activities:").grid(row=3, column=0, sticky="e")
        self.activities_entry = tk.Entry(root, width=20)
        self.activities_entry.grid(row=3, column=1)

        # Save button
        self.save_button = tk.Button(root, text="Save Plan", command=self.save_plan, width=20)
        self.save_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Listbox to display plans
        self.plans_listbox = tk.Listbox(root, width=40, height=5)
        self.plans_listbox.grid(row=5, column=0, columnspan=2, pady=10)

        # Label to display latest weather info
        self.weather_label = tk.Label(root, text="", fg="blue", wraplength=300, justify="left")
        self.weather_label.grid(row=6, column=0, columnspan=2)

        self.plans = []
        self.weather_api_key = "YOUR_OPENWEATHERMAP_API_KEY"  # <-- Insert your API key here

    def fetch_weather(self, city):
        """Fetch current weather for the given city using OpenWeatherMap API."""
        url = f"http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": self.weather_api_key,
            "units": "metric"
        }
        try:
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            weather = data["weather"][0]["description"].capitalize()
            temp = data["main"]["temp"]
            return f"{weather}, {temp}°C"
        except Exception as e:
            return "Weather info unavailable"

    def save_plan(self):
        destination = self.destination_entry.get()
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()
        activities = self.activities_entry.get()

        if not destination or not start_date or not end_date:
            messagebox.showwarning("Input Error", "Please fill in all required fields.")
            return

        # Fetch weather info for the destination
        weather_info = self.fetch_weather(destination)
        plan = f"{destination} | {start_date} - {end_date} | Activities: {activities} | Weather: {weather_info}"
        self.plans.append(plan)
        self.plans_listbox.insert(tk.END, plan)

        # Show weather info in a messagebox
        messagebox.showinfo("Weather Info", f"Current weather in {destination}: {weather_info}")

        # Also display weather info in the label
        self.weather_label.config(text=f"Current weather in {destination}: {weather_info}")

        # Clear entries
        self.destination_entry.delete(0, tk.END)
        self.start_date_entry.delete(0, tk.END)
        self.end_date_entry.delete(0, tk.END)
        self.activities_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = TravelPlannerApp(root)
    root.mainloop()
# This code creates a simple travel planner application using Tkinter.
# Users can input their travel plans, including destination, start and end dates, and activities.
# The app fetches current weather information for the destination using the OpenWeatherMap API.