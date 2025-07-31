from flask import Flask, render_template, request, jsonify
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# In-memory storage for demo; replace with persistent storage if needed
plans = []
next_id = 1

def fetch_weather(city):
    api_key = os.getenv("API_KEY")
    if not api_key:
        return "API key missing"
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}

    try:
        res = requests.get(url, params=params, timeout=7)
        res.raise_for_status()
        data = res.json()
        desc = data["weather"][0]["description"].capitalize()
        temp = data["main"]["temp"]
        return f"{desc}, {temp}°C"
    except Exception as e:
        print("Weather API error:", e)
        return "Weather info unavailable"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/plans', methods=['GET'])
def get_plans():
    return jsonify(plans)

@app.route('/add_plan', methods=['POST'])
def add_plan():
    global next_id
    data = request.form
    destination = data.get('destination')
    start_date = data.get('start_date')
    end_date = data.get('end_date')
    activities = data.get('activities')

    weather = fetch_weather(destination) if destination else "No weather data"

    plan = {
        'id': next_id,
        'destination': destination,
        'start_date': start_date,
        'end_date': end_date,
        'activities': activities,
        'weather': weather
    }
    plans.append(plan)
    next_id += 1
    return jsonify({'success': True, 'id': plan['id']})

@app.route('/plan_details/<int:plan_id>', methods=['GET'])
def plan_details(plan_id):
    plan = next((p for p in plans if p['id'] == plan_id), None)
    if plan:
        return jsonify(plan)
    return jsonify({'error': 'Plan not found'}), 404

@app.route('/edit_plan/<int:plan_id>', methods=['POST'])
def edit_plan(plan_id):
    data = request.form
    plan = next((p for p in plans if p['id'] == plan_id), None)
    if plan:
        destination = data.get('destination')
        plan['destination'] = destination
        plan['start_date'] = data.get('start_date')
        plan['end_date'] = data.get('end_date')
        plan['activities'] = data.get('activities')
        plan['weather'] = fetch_weather(destination) if destination else "No weather data"
        return jsonify({'success': True})
    return jsonify({'error': 'Plan not found'}), 404

@app.route('/delete_plan/<int:plan_id>', methods=['POST'])
def delete_plan(plan_id):
    global plans
    plans = [p for p in plans if p['id'] != plan_id]
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)
