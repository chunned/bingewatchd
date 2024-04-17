# BingeWatchd

BingeWatchd is a Python webapp for tracking the TV shows you watch. It was developed for the Introduction to Databases course project at Ontario Tech University.

## Self hosting
If you would like to self host the application, grab the [Docker Compose example](https://raw.githubusercontent.com/chunned/bingewatchd/docker/docker-compose-example.yml) and [nginx.conf](https://raw.githubusercontent.com/chunned/bingewatchd/docker/nginx.conf) files. 

Obtain an API key and token from [TMDB](https://www.themoviedb.org/settings/api), and enter them in the respective lines in the `docker-compose.yml` file. You can generate the SECRET_KEY with the following command:  `python -c "import os; print(os.urandom(12).hex())"` (or `python3`, depending on your system).

In `nginx.conf`, update the `server_name` with the domain you wish to use, and `proxy_pass` with IP of the host. 

Then, run `docker compose up -d`, navigate to `http://<DOMAIN|IP>:81` and create an account to get started. 

Please note that TLS is out of the scope of this project and should be configured elsewhere. However, you could also edit the Nginx configuration to include TLS certificates. 

## Database ER Diagram
![](ER%20Diagram.drawio.png)
