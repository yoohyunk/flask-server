from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

def hash_password(password):
        return PasswordHasher().hash(password)
    
def check_password(hash_password, password):
    try: 
        return PasswordHasher().verify(hash_password, password)
    except VerifyMismatchError:
        return False
         
    