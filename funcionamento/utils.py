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

def validate_permissions(user, metadata_path):
    if not os.path.exists(metadata_path):
        raise PermissionError("Erro: Metadados não encontrados. Permissão negada.")
    
    with open(metadata_path, 'r') as meta_file:
        metadata = meta_file.readlines()
    
    dono = None
    for line in metadata:
        if line.startswith("Proprietario:"):
            dono = line.split(":")[1].strip()
            print(f"Dono extraído dos metadados: {dono}")  # Debug
            break
    
    if dono != user["nome"]:
        print(f"Dono extraído dos metadados: {dono}") 
        raise PermissionError("Erro: Você não tem permissão para realizar esta ação.")
