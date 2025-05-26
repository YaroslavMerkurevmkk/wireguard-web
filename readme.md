# Manage wireguard clients from WEB

## Installation
Python3.x >= 3.11

Cloning repository to user's home directory

if python3.11 and python3.11-venv is installed in your system use:

```bash ./bin/setup.sh```


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

## Systemd Unit
! Change `user` and `PATH/TO/REPO`

```
[Unit]
Description=Wireguard client manager
After=network.target

[Service]
User=user
Group=user
WorkingDirectory=PATH/TO/REPO
ExecStart=PATH/TO/REPO/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:2222 web.wsgi

[Install]
WantedBy=multi-user.target
```

`sudo systemctl start unit_name.service` - start unit
`sudo systemctl enable unit_name.service` - enable autoloading

## Nginx

## Additions
Need permissions to staticfiles for www-data

`chmod o+x /home/user`

Using sudoers, acl (setfacl)

`setfacl -b /etc/wireguard`  (reset acl rules)

`setfacl -m u:tstu:rwx /etc/wireguard`  (set permission for user)
