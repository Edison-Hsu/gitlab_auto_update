import json as JSON
import urllib2
import re
import os
import logging
from logging.handlers import RotatingFileHandler

def get_current_tag(text):
    match = re.search(r"sameersbn/gitlab:.+", text)
    if match:
        return match.group(0).split(":")[1]
    else:
        return None

def write_new_tag(filedata, tag):
    filedata = re.sub(r'sameersbn/gitlab:.+', 'sameersbn/gitlab:' + tag, filedata)
    with open('docker-compose.yml', 'w') as f:
        f.write(filedata)

def get_latest_tag():
    response = urllib2.urlopen("https://hub.docker.com/v2/repositories/sameersbn/gitlab/tags/?page=1&page_size=2")
    j = response.read()
    json = JSON.loads(j)
    results = json["results"]
    for r in results:
        name = r["name"]
        if name != "latest": return name
        else: return None

def init_logger():
    log_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
    logFile = './gitlab_auto_update.log'

    my_handler = RotatingFileHandler(logFile, mode='a', maxBytes=5*1024*1024, 
                                     backupCount=2, encoding=None, delay=0)
    my_handler.setFormatter(log_formatter)
    my_handler.setLevel(logging.INFO)

    app_log = logging.getLogger('root')
    app_log.setLevel(logging.INFO)
    app_log.addHandler(my_handler)
    return app_log


# Main Function
logger = init_logger()
tag = get_latest_tag()

with open('docker-compose.yml', 'r') as f:
    filedata = f.read()
    ct = get_current_tag(filedata)

if ct is not None and ct == tag:
    logger.info("Do not need update. get tag from docker hub: {}. current tag: {}".format(tag, ct))
    exit(0)
else:
    write_new_tag(filedata, tag)
    logger.warn("Need update, system will reboot. get tag from docker hub: {}. current tag: {}".format(tag, ct))
    os.system('reboot')
