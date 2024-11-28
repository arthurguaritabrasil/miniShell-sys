import os
import hashlib

def generate_salt():
    """Gera um salt seguro para hashing."""
    return os.urandom(16)  # Salt gerado aleatoriamente com 16 bytes

def hash_password(password, salt):
    """Hash da senha utilizando SHA-512 com salt."""
    hasher = hashlib.sha512()
    hasher.update(salt)
    hasher.update(password.encode('utf-8'))
    return hasher.hexdigest()  # Retorna o hash gerado como string hexadecimal

def verify_password(password, stored_password):
    """Verifica se a senha fornecida é a mesma que a armazenada, utilizando salt e hash"""
    salt, stored_hash = stored_password.split(":")  # Separa salt e hash armazenados
    salt = bytes.fromhex(salt)  # Converte o salt de hexadecimal para bytes

    # Cria um novo hash utilizando o salt e a senha fornecida (SHA-512)
    new_hashed = hashlib.sha512()
    new_hashed.update(salt)  # Aplica o salt no hash
    new_hashed.update(password.encode('utf-8'))  # Aplica a senha fornecida no hash
    
    # Compara o novo hash gerado com o hash armazenado
    return new_hashed.hexdigest() == stored_hash 

def validate_permissions(user, owner):
    if user["username"] != owner:
        raise PermissionError("Permissão negada.")
