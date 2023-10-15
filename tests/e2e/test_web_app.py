import pytest
from flask import session

def test_register(client):
    # Check we can retrieve the register page
    response_code = client.get('/authentication/register').status_code
    assert response_code == 200
    # Check that we can register a user successfully, supplying a valid username and password
    response = client.post('/authentication/register', data={'username': 'Bob', 'password': 'fhrwjfohDh34'})
    assert response.location.endswith('/authentication/login')

def test_login(client, auth):
    # Check that we can retrieve login page
    response_code = client.get('/authentication/login').status_code
    assert response_code == 200
    response = auth.login()

def test_logout(client, auth):
    #This test checks that logging out clears a user sessions
    auth.login()
    with client:
        auth.logout()
        assert 'user_id' not in session

def test_index(client):
    # Check to see if we can retrieve the home page
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to Kelvin Games' in response.data

def test_login_required_to_review(client):
    game_id = 7940
    response = client.post(f'/review/{game_id}')
    assert response.status_code == 302
    assert response.headers['Location'] == '/authentication/login'

def test_view_user_profile(client, auth):
    # Test to see if we can view user profile when logged in
    response = client.get('/authentication/register')
    assert response.status_code == 200
    response = client.post('/authentication/register', data={'username': 'test_user', 'password': 'TestPass123'})
    assert response.status_code == 302
    response = client.get('/authentication/login')
    assert response.status_code == 200
    response = client.post('/authentication/login', data={'username': 'test_user', 'password': 'TestPass123'})
    response = client.get('/userprofile')
    assert response.status_code == 200

def test_view_user_profile_logged_out(client):
    response = client.get('/userprofile')
    assert response.status_code == 302

def test_register_user(client):
    # Test to check if we can register a user
    response = client.get('/authentication/register')
    assert response.status_code == 200
    response = client.post('/authentication/register', data={'username': 'test_user', 'password': 'TestPass123'})
    assert response.status_code == 302
    assert response.headers['Location'] == '/authentication/login'

def test_user_login(client):
    # Test to see user can register and log in successfully
    response = client.get('/authentication/register')
    assert response.status_code == 200
    response = client.post('/authentication/register', data={'username': 'test_user', 'password': 'TestPass123'})
    assert response.status_code == 302
    assert response.headers['Location'] == '/authentication/login'
    response = client.get('/authentication/login')
    assert response.status_code == 200
    response = client.post('/authentication/login', data={'username': 'test_user', 'password': 'TestPass123'})
    assert response.headers['Location'] == '/'

def test_user_login_incorrect_password(client):
    # Test to see if user enters incorrect password
    response = client.get('/authentication/register')
    assert response.status_code == 200
    response = client.post('/authentication/register', data={'username': 'test_user', 'password': 'TestPass123'})
    assert response.status_code == 302
    assert response.headers['Location'] == '/authentication/login'
    response = client.get('/authentication/login')
    assert response.status_code == 200
    response = client.post('/authentication/login', data={'username': 'test_user', 'password': 'testPass123'})
    assert b'The password provided is incorrect.'

def test_user_login_incorrect_username(client):
    # Test to see if user enters incorrect username
    response = client.get('/authentication/register')
    assert response.status_code == 200
    response = client.post('/authentication/register', data={'username': 'test_user', 'password': 'TestPass123'})
    assert response.status_code == 302
    assert response.headers['Location'] == '/authentication/login'
    response = client.get('/authentication/login')
    assert response.status_code == 200
    response = client.post('/authentication/login', data={'username': 'bob', 'password': 'testPass123'})
    assert b'The username entered does not exist.'

def test_user_registration_same_username(client):
    # Test to see if a user can use the same username as another user
    response = client.get('/authentication/register')
    assert response.status_code == 200
    response = client.post('/authentication/register', data={'username': 'test_user', 'password': 'TestPass123'})
    assert response.status_code == 302
    response = client.post('/authentication/register', data={'username': 'test_user', 'password': 'TestPass123'})
    assert b'That username is already in use, please provide another.'

def test_user_can_add_to_wishlist(client):
    # Test to see if user can add game to wishlist
    game_id = 7940
    response = client.get('/authentication/register')
    assert response.status_code == 200
    response = client.post('/authentication/register', data={'username': 'test_user', 'password': 'TestPass123'})
    assert response.status_code == 302
    response = client.get('/authentication/login')
    assert response.status_code == 200
    response = client.post('/authentication/login', data={'username': 'test_user', 'password': 'TestPass123'})
    response = client.post(f'/add_to_wishlist/{game_id}')
    assert response.status_code == 302
    assert response.headers['Location'] == '/userprofile'

def test_user_can_remove_from_wishlist(client):
    game_id = 7940
    response = client.get('/authentication/register')
    assert response.status_code == 200
    response = client.post('/authentication/register', data={'username': 'test_user', 'password': 'TestPass123'})
    assert response.status_code == 302
    response = client.get('/authentication/login')
    assert response.status_code == 200
    response = client.post('/authentication/login', data={'username': 'test_user', 'password': 'TestPass123'})
    response = client.post(f'/remove_from_wishlist/{game_id}')
    assert response.status_code == 302
    assert response.headers['Location'] == '/userprofile'

