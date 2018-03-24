# Web component

Boilerplate from
[Craicerjack/apache-flask](https://github.com/Craicerjack/apache-flask).

This file directory should be placed at `/home/ubuntu/webserver`. Then
`webserver.service` should be copied into `/etc/systemd/system/`. Use the
following commands to manage the server:

```bash
sudo systemctl daemon-reload  # read all .service files
sudo systemctl enable webserver  # start server on boot
sudo systemctl start webserver  # start server
sudo systemctl restart webserver  # update server with new changes
```
