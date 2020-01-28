import pytest
from flask import Flask
# from flask_bcrypt import Bcrypt
import sys
import os
import json

sys.path.append(sys.path[0])
from flaskr import get_flask_app

@pytest.fixture
def app():
    app = get_flask_app()
    # pytest-flask 미설치한 경우에는 client를 반환한다.
    # return app.test_client()
    # pytest-flask 설치시에는 app(Flask) 객체를 반환한다.
    return app

def get_header():
	return {
		'X-Requested-With' 	: 'XMLHttpRequest',
		'Content-Type'		: 'application/json',
	}

def test_index(client):
	res = client.get("/")
	assert res.status_code == 200
	# assert res.data == b'index page'
	
def test_login(client):
	headers 	= get_header()
	data		= json.dumps({
		'id'	: 'imcjpak1k@naver.com',
		'pw'	: '1234',
	})

	res = client.post("/user/login", data=data, headers=headers)
	assert res.status_code == 200, 'login'
	# assert res.data == b'login page'
	
def test_logout(client):
	req_data = {}
	
	# login
	headers 	= get_header()
	data 		= json.dumps(req_data)
	res = client.get("/user/login", data=data, headers=headers)
	assert res.status_code == 200, 'logout'

	# logout
	res = client.get("/user/logout")
	assert res.status_code == 200, 'logout'
	# assert res.data == b'logout page'