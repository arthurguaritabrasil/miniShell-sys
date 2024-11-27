import os
import json
import getpass

USERS_FILE = 'usuarios.json'

def load_users():
    """Carrega os dados dos usuários do arquivo JSON"""
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r') as f:
                data = json.load(f)
            return data.get("usuarios", [])  # Retorna uma lista vazia se 'usuarios' não existir
        except (json.JSONDecodeError, ValueError):  # Captura erros de leitura JSON ou se estiver vazio
            print("Erro ao carregar os dados de usuários. O arquivo pode estar corrompido ou vazio.")
            return []  # Retorna uma lista vazia em caso de erro
    return []

def save_users(users):
    """Salva os dados atualizados dos usuários no arquivo JSON"""
    with open(USERS_FILE, 'w') as f:
        json.dump({"usuarios": users}, f, indent=4)

def login():
    """Função de login"""
    users = load_users()  # Supondo que load_users carrega uma lista de dicionários
    nome = input("Digite o nome de usuário: ")
    senha = getpass.getpass("Digite a senha: ").strip()

    # Verifica se as credenciais são válidas
    for user in users:
        if user["nome"] == nome and user["senha"] == senha:
            print(f"Login bem-sucedido! Bem-vindo, {nome}.")
            
            # Adiciona o diretório atual, se não existir
            if "diretorio_atual" not in user:
                user["diretorio_atual"] = user["diretorio"]  # Inicializa com o diretório do usuário

            return user  # Retorna o dicionário de usuário, não apenas o nome
    
    print("Credenciais inválidas.")
    return None

def create_user_if_none():
    """Cria um novo usuário se nenhum for encontrado"""
    nome = input("Digite o nome de usuário: ")
    senha = getpass.getpass("Digite a senha: ").strip()
    diretorio = f"./data/files/{nome}"  # Diretório do usuário
    
    # Cria o diretório base para o novo usuário
    os.makedirs(diretorio, exist_ok=True)
    
    users = load_users()
    user = {"nome": nome, "senha": senha, "diretorio": diretorio, "diretorio_atual": diretorio}  # Inclui o 'diretorio_atual'
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
