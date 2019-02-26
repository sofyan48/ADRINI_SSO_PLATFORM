import pytest
from app import create_app
import requests
import json
import os

headers = dict()
expirehead = dict()

@pytest.fixture
def app():
    app = create_app()
    return app

@pytest.fixture(scope = 'session', autouse=True)
def tokenTest():
    url = os.getenv('APP_HOST', 'localhost')+":"+os.getenv('APP_PORT', 5000)
    response=requests.request("POST",url=url+'/admin/sign', data={'username': 'mongkey', 'password': 'mongkey'})
    result = response.json()
    tokensession=result['data']['apikey']
    global headers
    headers = {
            'Authorization' : str(tokensession)
        }
    print("ONLY ONCE")
    return headers

@pytest.fixture(scope = 'module', autouse=True)
def expiredToken():
    url = os.getenv('APP_HOST', 'localhost')+":"+os.getenv('APP_PORT', 5000)
    response=requests.request("POST",url=url+'/admin/sign', data={'username': 'fish', 'password': 'ikan'})
    result = response.json()
    extokensession=result['data']['apikey']
    global expirehead
    expirehead = {
            'Authorization' : str(extokensession)
        }
    print("ONLY ONCE")
    return expirehead

@pytest.fixture
def extokentest():
    return expirehead

@pytest.fixture(autouse=True)
def tokentest():
    return headers
