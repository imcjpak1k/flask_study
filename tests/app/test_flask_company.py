import pytest
import unittest
from flask import Flask
import json
import sys
import os

# sys.path.append(sys.path[0])
from flaskr import get_flask_app

def get_header():
	return {
		'X-Requested-With' 	: 'XMLHttpRequest',
		'Content-Type'		: 'application/json',
	}

@pytest.fixture
def app():
	app = get_flask_app()
	# pytest-flask 미설치한 경우에는 client를 반환한다.
	# return app.test_client()
	# pytest-flask 설치시에는 app(Flask) 객체를 반환한다.
	return app



def test_search(client):
	headers 	= get_header()

	data		= json.dumps({
		'id'	: 'imcjpak1k@naver.com',
		'pw'	: '1234',
	})
	res = client.post("/user/login", data=data, headers=headers)
	assert res.status_code == 200, 'login'

	data		= json.dumps({})
	res = client.post("/company/search", data=data, headers=headers)
	assert res.status_code == 200, 'state_code 200'

	res_data = json.loads(res.data)
	assert res_data, 'search'



def test_detail(client):
	headers 	= get_header()

	data		= json.dumps({
		'id'	: 'imcjpak1k@naver.com',
		'pw'	: '1234',
	})
	res = client.post("/user/login", data=data, headers=headers)
	assert res.status_code == 200, 'login'

	data		= json.dumps({
		'id' : 7
	})

	res = client.post("/company/detail", data=data, headers=headers)
	assert res.status_code == 200, 'state_code 200'

	res_data = json.loads(res.data)
	assert res_data, 'search'