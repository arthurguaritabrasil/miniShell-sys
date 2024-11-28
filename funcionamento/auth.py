import os
import getpass
from funcionamento.utils import generate_salt, hash_password, verify_password

USERS_FILE = './data/users.txt'

def load_users():
    users = []
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue 
                parts = line.split(':')
                if len(parts) != 4:  
                    print(f"Atenção: Linha malformada no arquivo de usuários: '{line}'")
                    continue
                nome, salt, hashed_password, diretorio = parts
                users.append({
                    "nome": nome,
                    "senha": f"{salt}:{hashed_password}",
                    "diretorio": diretorio,
                    "diretorio_atual": diretorio
                })
    return users


def save_users(users):
    with open(USERS_FILE, 'w') as f:
        for user in users:
            nome = user["nome"]
            salt, hashed_password = user["senha"].split(':')
            diretorio = user["diretorio"]
            f.write(f"{nome}:{salt}:{hashed_password}:{diretorio}\n")


def login():
    print(f"PID do processo atual: {os.getpid()}")
    users = load_users()
    nome = input("Digite o nome de usuário: ")
    senha = getpass.getpass("Digite a senha: ").strip()

    for user in users:
        if user["nome"] == nome:
            print(f"Verificando senha para {nome}...")
            if verify_password(senha, user["senha"]):
                print(f"Login bem-sucedido! Bem-vindo, {nome}.")

                if "diretorio_atual" not in user:
                    user["diretorio_atual"] = user["diretorio"]

                return user
            else:
                print("Senha incorreta.")
                return None
    
    print("Credenciais inválidas.")
    return None

def create_user_if_none():
    nome = input("Digite o nome de usuário: ")
    senha = getpass.getpass("Digite a senha: ").strip()
    diretorio = f"./data/files/{nome}"
    os.makedirs(diretorio, exist_ok=True)
    
    salt = generate_salt()
    hashed_password = hash_password(senha, salt)
    
    user = {"nome": nome, "senha": f"{salt.hex()}:{hashed_password}", "diretorio": diretorio, "diretorio_atual": diretorio}
    
    users = load_users()
    users.append(user)
    save_users(users)
    print(f"Usuário {nome} criado com sucesso!")
    return user

def create_or_login_user():
    users = load_users()
    
    if not users:
        print("Nenhum usuário encontrado. Criando um novo usuário...")
        print(f"PID do processo atual: {os.getpid()}")
        return create_user_if_none()
    
    print("Já existem usuários registrados.")
    choice = input("Deseja fazer login ou criar um novo usuário? (login/criar): ").strip().lower()
    
    if choice == "login":
        return login()
    elif choice == "criar":
        return create_user_if_none()
    else:
        print("Opção inválida. Por favor, tente novamente.")
        return create_or_login_user()