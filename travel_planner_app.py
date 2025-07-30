#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Travel Planner App with Weather and Activity Logger
Displays plan info in terminal too.
"""

import tkinter as tk
from tkinter import messagebox
from dotenv import load_dotenv
load_dotenv()
import os
import requests
import json



class TravelPlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Travel Planner App")
        self.root.geometry("420x540")

        # Input fields
        tk.Label(root, text="Destination:").grid(row=0, column=0, sticky="e")
        self.destination_entry = tk.Entry(root, width=30)
        self.destination_entry.grid(row=0, column=1)

        tk.Label(root, text="Start Date:").grid(row=1, column=0, sticky="e")
        self.start_date_entry = tk.Entry(root, width=30)
        self.start_date_entry.grid(row=1, column=1)

        tk.Label(root, text="End Date:").grid(row=2, column=0, sticky="e")
        self.end_date_entry = tk.Entry(root, width=30)
        self.end_date_entry.grid(row=2, column=1)

        tk.Label(root, text="Activities:").grid(row=3, column=0, sticky="e")
        self.activities_entry = tk.Entry(root, width=30)
        self.activities_entry.grid(row=3, column=1)

        self.save_button = tk.Button(root, text="Save Plan", command=self.save_plan, width=35)
        self.save_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.edit_button = tk.Button(root, text="Edit Selected Plan", command=self.edit_plan, width=35)
        self.edit_button.grid(row=5, column=0, columnspan=2, pady=5)

        self.plans_listbox = tk.Listbox(root, width=55, height=6)
        self.plans_listbox.grid(row=6, column=0, columnspan=2)
        self.plans_listbox.bind('<<ListboxSelect>>', self.show_plan_details)

        self.weather_label = tk.Label(root, text="", fg="blue", wraplength=390, justify="left")
        self.weather_label.grid(row=7, column=0, columnspan=2)

        self.plans = []
        self.filename = "travel_plans.json"

        self.load_plans()

    def fetch_weather(self, city):
        api_key = os.getenv("API_KEY")  
        url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": api_key,
            "units": "metric"
        }

        try:
            res = requests.get(url, params=params, timeout=7)
            res.raise_for_status()
            data = res.json()
            desc = data["weather"][0]["description"].capitalize()
            temp = data["main"]["temp"]
            return f"{desc}, {temp}°C"
        except requests.RequestException as e:
            print("Weather API error:", e)
            return "Weather info unavailable"

    def save_plan(self):
        destination = self.destination_entry.get().strip()
        start_date = self.start_date_entry.get().strip()
        end_date = self.end_date_entry.get().strip()
        activities = self.activities_entry.get().strip()

        if not destination or not start_date or not end_date:
            messagebox.showwarning("Input Error", "Please fill in all required fields.")
            return

        weather_info = self.fetch_weather(destination)

        plan = {
            "destination": destination,
            "start_date": start_date,
            "end_date": end_date,
            "activities": activities,
            "weather": weather_info
        }

        self.plans.append(plan)
        self.plans_listbox.insert(tk.END, f"{destination} | {start_date} - {end_date}")
        self.save_to_file()

        self.display_plan_details(plan)
        print("\n--- New Travel Plan Saved ---")
        self.clear_fields()

    def show_plan_details(self, event):
        index = self.plans_listbox.curselection()
        if index:
            i = index[0]
            plan = self.plans[i]
            self.display_plan_details(plan)
            print("\n--- Viewing Travel Plan ---")
            print(plan)

    def display_plan_details(self, plan):
        details = (
            f"Plan for {plan['destination']}:\n"
            f"Dates: {plan['start_date']} - {plan['end_date']}\n"
            f"Activities: {plan['activities']}\n"
            f"Weather: {plan['weather']}"
        )
        self.weather_label.config(text=details)

    def edit_plan(self):
        index = self.plans_listbox.curselection()
        if not index:
            messagebox.showinfo("Select Plan", "Please select a plan to edit.")
            return

        i = index[0]
        plan = self.plans[i]

        self.destination_entry.delete(0, tk.END)
        self.destination_entry.insert(0, plan["destination"])

        self.start_date_entry.delete(0, tk.END)
        self.start_date_entry.insert(0, plan["start_date"])

        self.end_date_entry.delete(0, tk.END)
        self.end_date_entry.insert(0, plan["end_date"])

        self.activities_entry.delete(0, tk.END)
        self.activities_entry.insert(0, plan["activities"])

        def update_plan():
            destination = self.destination_entry.get().strip()
            start_date = self.start_date_entry.get().strip()
            end_date = self.end_date_entry.get().strip()
            activities = self.activities_entry.get().strip()

            if not destination or not start_date or not end_date:
                messagebox.showwarning("Input Error", "Please fill in all required fields.")
                return

            weather_info = self.fetch_weather(destination)

            updated_plan = {
                "destination": destination,
                "start_date": start_date,
                "end_date": end_date,
                "activities": activities,
                "weather": weather_info
            }

            self.plans[i] = updated_plan
            self.save_to_file()

            self.plans_listbox.delete(i)
            self.plans_listbox.insert(i, f"{destination} | {start_date} - {end_date}")

            self.weather_label.config(text="Plan updated successfully.")
            print("\n--- Plan Updated ---")
            print(updated_plan)

            self.save_button.config(command=self.save_plan)
            self.clear_fields()

        self.save_button.config(command=update_plan)

    def clear_fields(self):
        self.destination_entry.delete(0, tk.END)
        self.start_date_entry.delete(0, tk.END)
        self.end_date_entry.delete(0, tk.END)
        self.activities_entry.delete(0, tk.END)

    def save_to_file(self):
        try:
            with open(self.filename, "w") as f:
                json.dump(self.plans, f, indent=4)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save plans: {e}")

    def load_plans(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as f:
                    self.plans = json.load(f)
                    for plan in self.plans:
                        self.plans_listbox.insert(
                            tk.END, f"{plan['destination']} | {plan['start_date']} - {plan['end_date']}"
                        )
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load plans: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = TravelPlannerApp(root)
    root.mainloop()
