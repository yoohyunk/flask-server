from flask_server.utils.jwt import *

def test_create_jwt():
    jwt = create_jwt('test')
    assert jwt is not None

def test_verify_jwt():
    jwt = create_jwt('test')
    user = verify_jwt(jwt)
    assert user['user_email'] == 'test'
    assert user['error'] == None
   

def test_verify_jwt_not_valid():
    jwt = create_jwt('test')
    invalid_jwt = jwt + 'invalid'
    user = verify_jwt(invalid_jwt)
    assert user['user_email'] == None
    assert user['error'] == 'Invalid token'

