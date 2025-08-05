 Travel Planner App

A Flask-based web application that helps users create, view, edit, and delete travel plans. It supports basic planning features and uses an external API to enhance the user experience.



 Live Demo

Access the app via the load balancer

🔗 [http://35.174.154.54](http://35.174.154.54)

---

Local Setup

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/travel-planner-app.git
cd travel-planner-app
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app locally

```bash
flask run
```

By default, the app runs on `http://127.0.0.1:5000/`.

---

 Deployment on Web01 and Web02

1. **Copy project files** to both servers (via Git or `scp`)

2. **Set up Python environment**

```bash
sudo apt update
sudo apt install python3-venv python3-pip -y
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. **Create a systemd service**

```bash
sudo nano /etc/systemd/system/travel_planner.service
```

Paste the following:

```ini
[Unit]
Description=Gunicorn instance to serve travel_planner
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/travel-planner-app
ExecStart=/home/ubuntu/travel-planner-app/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:8000 main:app

[Install]
WantedBy=multi-user.target
```

4. **Enable and start the service**

```bash
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl start travel_planner
sudo systemctl enable travel_planner
```

5. **Install and configure Nginx**

```bash
sudo apt install nginx -y
sudo nano /etc/nginx/sites-available/travel_planner
```

Paste:

```nginx
server {
    listen 80;
    server_name <WEB_SERVER_IP>;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Then:

```bash
sudo ln -s /etc/nginx/sites-available/travel_planner /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl reload nginx
```

---

## ⚖️ Load Balancer (Nginx)

1. **On the load balancer (Lb01), configure Nginx**


sudo nano /etc/nginx/conf.d/load_balance.conf


Paste:

nginx
upstream travel_backend {
    ip_hash;
    server 54.88.46.147:80;  # Web01
    server 52.90.91.120:80;  # Web02
}

server {
    listen 80;

    location / {
        proxy_pass http://travel_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}


2. Disable default site (if needed)


sudo rm /etc/nginx/sites-enabled/default


3. Test and reload


sudo nginx -t
sudo systemctl reload nginx


---

 Testing Load Balancing

1. Visit `http://35.174.154.54` in your browser.
2. Add a plan. Reload the page.
3. You should remain on the same server (thanks to `ip_hash` sticky sessions).
4. To confirm balancing, check logs on each server or add a custom header in Nginx config.

---

 Secrets and API Keys

 API keys are not hard-coded
 Use a `.env` file and `python-dotenv` to load them
 Make sure `.env` is excluded from Git via `.gitignore`

---

🔗 APIs Used

 1. openweathermap.org

  Purpose: Fetches current weather data for travel destinations
  Endpoint Example:

  ```
 https://api.openweathermap.org/data/2.5/weather?q=Kigali&appid=YOUR_API_KEY&units=metric

  ```
* No API key needed

Credit: [https://home.openweathermap.org/api_keys) for the free service.

---

 Development Challenges

 Flask App Not Detected

Problem: `flask run` failed to detect the app
Fix: Exported `FLASK_APP` variable:

  ```bash
  export FLASK_APP=main.py
  ```

Virtualenv Activation on Windows

Problem: `source venv/bin/activate` failed
  Fix: Used `source venv/Scripts/activate` instead

Load Balancing Debugging

Problem: Hard to verify round-robin behavior
Fix: Added custom response headers on each backend server using Nginx:

  ```nginx
  add_header X-Served-By Web01;  # change per server
  ```

---

 Project Structure

```
travel-planner-app/
├── templates/
│   └── index.html
├── static/
├── main.py
├── requirements.txt
└── README.md
```

---
License

This project is open-source and free to use for learning purposes.

---

Let me know if you'd like me to:

* Plug in your real GitHub repo link
* Add database setup (SQLite or PostgreSQL)
* Help generate a sample `.env` file

I can also export this to a `.md` file if you want to copy it directly into your GitHub repo.
