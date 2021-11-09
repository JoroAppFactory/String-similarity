# General
import requests
import os

# Services
from resources.services.file_service import read_file


# Vasko API
def detect_text(path, filename):
    credentials = read_file(f'{os.getcwd()}/credentials.json')
    url = credentials['google']['url']

    files = {'image': open(path, 'rb')}
    request = requests.post(url, {
        "name": "image",
        "filename": filename
    }, files=files).json()

    request = ' '.join(request['labels']).lower().replace("\n", " ")
    return request
