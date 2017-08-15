# Gitlab docker image auto update

## Origin

I use [sameersbn/gitlab](https://hub.docker.com/r/sameersbn/gitlab/) docker image. I need manually update docker image version in docker-compose.yml before I wrote the python script.

## Usage

Put the script to the same path with docker-compose.yml file, and set the crontab job to run the script periodically. This script will request docker hub tag api and get the latest version. If version changed, it will auto update and restart the docker container.

```
main.py ------- script file

docker-compose.yml ----- docker-compose template file
```


### run the script

```python
python main.py
```
