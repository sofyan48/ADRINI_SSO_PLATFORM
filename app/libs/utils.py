from app import root_dir
from datetime import datetime
import json, requests


def timeset():
    return datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

def mkdir(dir):
    if not os.path.isdir(dir):
        os.makedirs(dir)

def read_file(file):
    with open(file, 'r') as outfile:
        return outfile.read()

def list_dir(dirname):
    listdir = list()
    for root, dirs, files in os.walk(dirname):
        for file in files:
            listdir.append(os.path.join(root, file))
    return listdir

def send_http(url, data):
    json_data = json.dumps(data)
    send = requests.post(url, data=json_data)
    respons = send.json()
    return respons

def get_http(url, param=None, header=None):
    json_data = None
    if param:
        json_data = param
    get_func = requests.get(url, params=json_data, headers=header)
    data = get_func.json()
    return data