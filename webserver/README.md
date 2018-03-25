# Web component

Boilerplate from
[Craicerjack/apache-flask](https://github.com/Craicerjack/apache-flask).

# Updating the server

- caution: the local database will overwrite the remote database unless it is
  deleted before running the command.
- copy the data over: `cd webserver; scp -r apache-flask.conf apache-flask.wsgi
  app docker-compose.yml Dockerfile README.md run.py
  root@ec2-54-175-172-96.compute-1.amazonaws.com:/var/www/apache-flask/`
- View logs: `journalctl --follow`/`journalctl --since='5 minutes ago'`/`cat
  ~/webserver-log/apache/error.log`.
