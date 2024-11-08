from argon2 import PasswordHasher

def hash_password(password):
        return PasswordHasher().hash(password)
    
def check_password(hash_password, password):
    return PasswordHasher().verify(hash_password, password)