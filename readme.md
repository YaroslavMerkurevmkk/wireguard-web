# Manage WireGuard Clients via Web Interface


## 📦 Installation

Install required packages (for Debian-based systems):

```bash
apt update
apt install wireguard wireguard-tools
```

Requires: Python 3.11 or higher

Clone the repository into your home directory.

If `python3.11` and `python3.11-venv` are installed:
```bash 
./bin/setup.sh
```

Else:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```


## ⚙️ Configuration

`config.json` example:

```json
{
  "SECRET_KEY": "",
  "DEBUG": false,
  "ALLOWED_HOSTS": [],
  "CSRF_TRUSTED_ORIGINS": [],
  "WIREGUARD_DIR": "/etc/wireguard",
  "WIREGUARD_PORT": 51830,
  "LOG_DIR": "logs"
}
```


## 🚀 Running the Django App
Run the following commands:

`python manage.py makemigrations`

`python manage.py migrate`

`python manage.py createsuperuser`

`python manage.py collectstatic`


## 🛠️ systemd Unit Example

Edit the unit file with the correct username and path:

```
[Unit]
Description=WireGuard Client Manager
After=network.target

[Service]
User=your_username
Group=your_username
WorkingDirectory=/home/your_username/wireguard-web
ExecStart=/home/your_username/wireguard-web/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:2222 web.wsgi

[Install]
WantedBy=multi-user.target
```

To start and enable the service:

`sudo systemctl start wireguard-web.service`

`sudo systemctl enable wireguard-web.service`


## 🌐 Nginx Configuration

Secure your app using Let's Encrypt and restrict admin access.

```
server {
    listen 10000 ssl;
    server_name example.com;

    ssl_certificate PATH/fullchain.pem; # managed by Certbot
    ssl_certificate_key PAHT/privkey.pem; # managed by Certbot

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'HIGH:!aNULL:!MD5';

    location /admin/ {
        allow 10.0.0.2;       # allow trusted IP only
        deny all;
        proxy_pass http://127.0.0.1:2222;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /home/your_username/wireguard-web/staticfiles/;
        autoindex off;
        expires 30d;
        add_header Cache-Control "public, max-age=2592000";
    }
}
```

## 📁 File Permissions
Grant access to static files and WireGuard config:

`chmod o+x /home/your_username`

Use ACL to give Django access to /etc/wireguard:

`setfacl -b /etc/wireguard` # Reset ACL

`setfacl -m u:your_username:rwx /etc/wireguard`
