#This program contains all functions needed to fetch a list of images and download them

import json
import logging
import os
from pathlib import Path
from tkinter import W
from urllib.request import urlopen, Request

logger = logging.getLogger(__name__)

types = {'image/jpeg', 'image/png'}

def get_links(client_id):
    headers = {'Authorisation': 'ClientID {}'.format(client_id)}
    req = Request('https://imgur.com/t/aww?source=featured_tag_module', headers=headers, method='GET')
    with urlopen(req) as resp:
        data = json.loads(resp.read().decode('utf-8'))
    for item in data['data']:
        if 'type' in item and item['type'] in types:
            return item['link']

def download_link(directory, link):
    download_path = directory/os.path.basename(link)
    with urlopen(link) as image, download_path.open('wb') as f:
        f.write(image.read())
    logger.info('Download %s', link)

def setup_download_dir():
    download_dir = Path('images')
    if not download_dir.exists():
        download_dir.mkdir()
    return download_dir