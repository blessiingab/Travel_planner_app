# Travel Planner Web App

A simple travel planner web application built with Flask. Users can create and manage travel plans that include trips and weather info. Deployed easily using Docker and load-balanced with Nginx.

---

## 🔧 Features

- Flask‑based web app (`travel_planner_app.py`)
- Static HTML/CSS frontend under `/templates` and `/static`
- Stores travel plans in a local JSON file (`travel_plans.json`)
- CLI and web interface, with ability to add/view/delete trips via browser

---

## 🚀 Local Setup / Development

1. **Clone the repo**  
   ```bash
   git clone https://github.com/blessiingab/Travel_planner_app.git
   cd Travel_planner_app
Expense Tracker
A Flask-based expense tracking web application allowing users to add expenses, filter reports by date, and convert currencies.

Local Setup
Clone the repository:

git clone https://github.com/yourusername/expense-tracker.git
cd expense-tracker
Create and activate virtual environment:

python3 -m venv venv
source venv/bin/activate
Install dependencies:

pip install -r requirements.txt
Run the app locally:

flask run
Access the app at https://irakoze24.tech/

Deployment on Web01 and Web02
Copy project files to both servers via SSH or Git.

On each server:

sudo apt update
sudo apt install python3-venv python3-pip -y
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
Create a systemd service file at:

sudo nano /etc/systemd/system/expense_tracker.service

Paste the following:

[Unit]
Description=Gunicorn instance to serve expense_tracker
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/expense_tracker
ExecStart=/home/ubuntu/expense_tracker/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 main:app

[Install]
WantedBy=multi-user.target
Start and enable the service:

sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl start expense_tracker
sudo systemctl enable expense_tracker
Install and configure Nginx:

sudo apt install nginx -y

Then:

sudo nano /etc/nginx/sites-available/expense_tracker

Paste:

server {
    listen 80;
    server_name <web-server-IP>;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

Enable and reload:


sudo ln -s /etc/nginx/sites-available/expense_tracker /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl reload nginx
Load Balancer (HAProxy) Configuration
On the load balancer server:

SSH into lb-01 ssh -i ~/.ssh/school ubuntu@44.204.76.162

sudo apt install haproxy -y

Edit the HAProxy config:

sudo nano /etc/haproxy/haproxy.cfg

Add at the bottom:

frontend http_front bind *:80 default_backend http_back

backend http_back balance roundrobin server web01 52.70.25.100:80 check server web02 34.226.246.26:80 check

Restart HAProxy:

sudo systemctl restart haproxy

Testing Load Balancer: curl -I http://44.204.76.162

Visit the Load Balancer’s IP in a browser: http://44.204.76.162

Refresh the page multiple times.

Observe logs or add a unique header per server to confirm that requests alternate between Web01 and Web02.

APIs Used
1. ExchangeRate.host
Used to fetch real-time currency conversion rates for user expenses. It is a free, no-authentication-required API based on the European Central Bank and other sources.

Endpoint: https://api.exchangerate.host/convert?from=USD&to=EUR&amount=1

Features Used:
Currency conversion
Historical exchange rates
Credit: ExchangeRate.host for providing a free, reliable API.

2. Google Sheets API
Used (via gspread and oauth2client) to log or sync expenses in a Google Sheet for backup or collaborative reporting.

Features Used:
Append rows
Read and write values
Authenticate using service account credentials
Credit: Google Developers for the Google Sheets API and the gspread Python wrapper.

Development Challenges & Solutions
1. Activating Virtual Environment on Windows**
Challenge: Activation failed with source venv/bin/activate.
Solution: Used the correct Windows path: source venv/Scripts/activate.
2. Flask Not Recognizing App**
Challenge: Error: Could not locate a Flask application.
Solution: Exported the FLASK_APP variable:
export FLASK_APP=main.py

### 2. Load Balancer Testing**
- **Challenge:** Verifying round-robin load balancing on HAProxy.*.
- **Solution:**  Added unique response headers in Nginx config (e.g., X-Served-By) to confirm switching between web servers.
About
No description, website, or topics provided.
Resources
 Readme
 Activity
Stars
 0 stars
Watchers
 0 watching
Forks
 0 forks
Report repository
Releases
No releases published
Packages
No packages published
Languages
Python
72.8%
 
HTML
27.2%
Footer
© 2025 GitHub, Inc