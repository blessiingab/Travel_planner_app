Travel Planner App
A simple web application to create, view, edit, and delete travel plans. It is deployed on two web servers and load balanced using Nginx.

Overview
The app runs on two Ubuntu servers:

Web01: 54.88.46.147

Web02: 52.90.91.120

Nginx on the load balancer (35.174.154.54) distributes requests between these two servers.

Sticky sessions are enabled to ensure users remain connected to the same server during their session.

Deployment Instructions
On Web01 and Web02
Clone the repo

bash
Copy
Edit
git clone https://github.com/blessiingab/travel-planner-app.git
cd travel-planner-app
Install dependencies

Make sure Python3 and pip are installed:

bash
Copy
Edit
sudo apt update
sudo apt install python3 python3-pip -y
Install Python packages

bash
Copy
Edit
pip3 install -r requirements.txt
Run the app

Assuming your app runs on port 5000:

bash
Copy
Edit
python3 app.py
Or if you have a startup script, use that.

Make sure the app is listening on all interfaces (0.0.0.0), so it’s reachable by the load balancer.

On Load Balancer (Lb01)
Configure Nginx

Create or edit /etc/nginx/conf.d/load_balance.conf with:

nginx
Copy
Edit
upstream travel_backend {
    ip_hash;
    server 54.88.46.147:5000;
    server 52.90.91.120:5000;
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
Disable default site

bash
Copy
Edit
sudo rm /etc/nginx/sites-enabled/default
Test and reload Nginx

bash
Copy
Edit
sudo nginx -t
sudo systemctl reload nginx
How to Test
Access the app via http://35.174.154.54

Add, view, edit, and delete plans

Confirm plans persist during your session (sticky sessions keep you on the same backend server)

For true persistence across servers, consider implementing shared database (optional)

Handling API Keys & Secrets
Store API keys in a .env file or environment variables on each server

Never commit .env or keys to GitHub

Use libraries like python-dotenv to load environment variables securely

Challenges & Notes
Plans are stored locally on each server; switching servers during a session might cause missing data

Sticky sessions mitigate this but are not a perfect solution

For full reliability, move to a centralized database system

Credits
API used: [Name & URL]

Flask, Nginx, and other open-source tools used in this project


