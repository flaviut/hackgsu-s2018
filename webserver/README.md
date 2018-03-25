# Web component

Boilerplate from
[Craicerjack/apache-flask](https://github.com/Craicerjack/apache-flask).

# Updating the server

## On your computer

- copy the data over: `scp -r ./webserver
  root@ec2-54-175-172-96.compute-1.amazonaws.com:/etc/docker/compose/webserver`
- ssh in: `ssh ubuntu@ec2-54-175-172-96.compute-1.amazonaws.com`

## on the server

- Stop the server: `sudo systemctl stop docker-compose@webserver`
- Delete the server: `sudo docker rmi webserver_web`
- Fix permissions on the files: `sudo chmod -R o+r,g+rw /etc/docker/compose/*`
- Restart the server: `sudo systemctl start docker-compose@webserver`
- View logs: `journalctl --follow`/`journalctl --since='5 minutes ago'`
