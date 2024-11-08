import jwt
import os


def create_jwt(user_email: str):
    secret = get_jwt_secret()
    
    encoded_jwt = jwt.encode({'user_email': user_email}, secret, algorithm='HS256')

    return encoded_jwt

def verify_jwt(encoded_jwt: str):
    secret = get_jwt_secret()
    try:
        decoded_jwt = jwt.decode(encoded_jwt, secret, algorithms=['HS256'])
        return {'error' : None, 'user_email': decoded_jwt['user_email']}
    except jwt.ExpiredSignatureError:
        return {'error': 'Expired token', 'user_email': None}
    except jwt.InvalidTokenError:
        return {'error': 'Invalid token', 'user_email': None}    
        
    

def get_jwt_secret():
    secret =  os.getenv('JWT_secret')
    if secret is None:
        raise ValueError("Invalid environment")
    return secret