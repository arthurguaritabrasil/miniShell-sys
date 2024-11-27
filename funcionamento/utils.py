import os
import hashlib

def generate_salt():
    """Gera um salt seguro para hashing."""
    return os.urandom(16)

def hash_password(password, salt):
    """Hash da senha utilizando SHA-512 com salt."""
    hasher = hashlib.sha512()
    hasher.update(salt)
    hasher.update(password.encode('utf-8'))
    return hasher.hexdigest()


def verify_password(password, stored_password):
    salt, hashed = stored_password.split(":")
    new_hashed = hashlib.pbkdf2_hmac("sha512", password.encode(), bytes.fromhex(salt), 100000)
    return new_hashed.hex() == hashed

def allocate_memory(size):
    # Simulação de algoritmo de alocação de memória (exemplo: best fit)
    return f"Allocated {size} bytes"

def deallocate_memory(memory):
    print(f"{memory} desalocado.")

def validate_permissions(user, owner):
    if user["username"] != owner:
        raise PermissionError("Permissão negada.")
