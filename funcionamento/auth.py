import os
import json
import getpass
from funcionamento.utils import generate_salt, hash_password, verify_password

USERS_FILE = './data/users.json'

def load_users():
    """Carrega os dados dos usuários do arquivo JSON"""
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r') as f:
                content = f.read().strip()  # Lê o conteúdo do arquivo
                if not content:  # Se o conteúdo estiver vazio
                    return []  # Retorna uma lista vazia
                data = json.loads(content)  # Caso contrário, tenta fazer o parsing do JSON
            # Verifica se 'usuarios' existe e se é uma lista, senão retorna uma lista vazia
            return data.get("usuarios", [])
        except json.JSONDecodeError as e:
            print(f"Erro ao carregar os dados de usuários: {e}")
            return []  # Retorna uma lista vazia se o arquivo JSON estiver corrompido
    else:
        # Se o arquivo não existir, retorna uma lista vazia
        return []

def save_users(users):
    """Salva os dados atualizados dos usuários no arquivo JSON"""
    with open(USERS_FILE, 'w') as f:
        json.dump({"usuarios": users}, f, indent=4)

def login():
    """Função de login"""
    users = load_users()  # Carrega os usuários
    nome = input("Digite o nome de usuário: ")
    senha = getpass.getpass("Digite a senha: ").strip()

    # Verifica se as credenciais são válidas
    for user in users:
        if user["nome"] == nome:
            print(f"Verificando senha para {nome}...")

            # Verificação de senha utilizando a função verify_password
            if verify_password(senha, user["senha"]):
                print(f"Login bem-sucedido! Bem-vindo, {nome}.")

                # Se 'diretorio_atual' não estiver presente, cria com o valor de 'diretorio'
                if "diretorio_atual" not in user:
                    user["diretorio_atual"] = user["diretorio"]  # Adiciona a chave

                return user  # Retorna o dicionário de usuário, não apenas o nome
            else:
                print("Senha incorreta.")
                return None
    
    print("Credenciais inválidas.")
    return None

def create_user_if_none():
    """Cria um novo usuário se nenhum for encontrado"""
    nome = input("Digite o nome de usuário: ")
    senha = getpass.getpass("Digite a senha: ").strip()
    diretorio = f"./data/files/{nome}"  # Diretório do usuário
    
    # Cria o diretório base para o novo usuário
    os.makedirs(diretorio, exist_ok=True)
    
    # Gerar salt e hash da senha
    salt = generate_salt()
    hashed_password = hash_password(senha, salt)
    
    # Criar o novo usuário com a chave 'diretorio_atual'
    user = {"nome": nome, "senha": f"{salt.hex()}:{hashed_password}", "diretorio": diretorio, "diretorio_atual": diretorio}
    
    users = load_users()
    users.append(user)
    save_users(users)
    print(f"Usuário {nome} criado com sucesso!")
    return user  # Retorna o dicionário do novo usuário

def create_or_login_user():
    """Chama o login ou cria um novo usuário caso não exista nenhum"""
    users = load_users()
    
    if not users:  # Caso não exista nenhum usuário
        print("Nenhum usuário encontrado. Criando um novo usuário...")
        return create_user_if_none()
    
    print("Já existem usuários registrados.")
    choice = input("Deseja fazer login ou criar um novo usuário? (login/criar): ").strip().lower()
    
    if choice == "login":
        return login()  # Retorna o usuário autenticado
    elif choice == "criar":
        return create_user_if_none()  # Cria um novo usuário
    else:
        print("Opção inválida. Por favor, tente novamente.")
        return create_or_login_user()  # Repete a escolha
