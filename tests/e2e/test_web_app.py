import pytest
from flask import session

def test_register(client):
    # Check we can retrieve the register page
    response_code = client.get('/authentication/register').status_code
    assert response_code == 200
    # Check that we can register a user successfully, supplying a valid username and password
    response = client.post('/authentication/register', data={'username': 'Bob', 'password': 'fhrwjfohDh34'})
    assert response.location.endswith('/authentication/login')

def test_login(client):
    # Check that we can retrieve login page
    response_code = client.get('authentication/login').status_code
    assert response_code == 200




