import os
import hashlib

def generate_salt():
    return os.urandom(16) 

def hash_password(password, salt):
    hasher = hashlib.sha512()
    hasher.update(salt)
    hasher.update(password.encode('utf-8'))
    return hasher.hexdigest() 

def verify_password(password, stored_password):

    salt, stored_hash = stored_password.split(":")  
    salt = bytes.fromhex(salt)  

    new_hashed = hashlib.sha512()
    new_hashed.update(salt)  
    new_hashed.update(password.encode('utf-8'))  

    return new_hashed.hexdigest() == stored_hash 

def validate_permissions(user, owner):
    if user["username"] != owner:
        raise PermissionError("Permissão negada.")
