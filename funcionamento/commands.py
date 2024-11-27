import os
import shutil
from funcionamento.utils import validate_permissions

BASE_DIR = "./data/files"  # Diretório base para todas as operações de arquivos

def ensure_base_directory():
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)  # Cria a pasta 'files' caso não exista

def execute_command(command, user):
    parts = command.split()
    cmd = parts[0].lower()

    if cmd == "listar" or cmd == "ls":
        directory = parts[1] if len(parts) > 1 else "."
        return list_directory(directory, user)

    elif cmd.startswith("criar"):
        if "arquivo" in parts:
            return create_file(parts[2], user)
        elif "diretorio" in parts:
            return create_directory(parts[2], user)
    elif cmd == "cd":  # Comando cd
        if len(parts) > 1:
            return change_directory(parts[1], user)
        else:
            print("Erro: Nenhum diretório especificado.")
        return
    elif cmd.startswith("apagar"):
        if "arquivo" in parts:
            return delete_file(parts[2], user)
        elif "diretorio" in parts:
            force = "--force" in parts
            return delete_directory(parts[2], user, force)

    elif cmd == "exit" or cmd == "sair":
        return exit_shell()
    elif cmd == "clear" or cmd == "cls":
        return clear_screen()
    else:
        print(f"Comando desconhecido: {cmd}")
        return

def list_directory(directory, user):
    """Lista o conteúdo de um diretório dentro do diretório do usuário"""
    if not isinstance(user, dict):
        print("Erro: Usuário não encontrado.")
        return

    # Verifica se o diretório a ser listado é dentro do diretório do usuário
    user_directory = user["diretorio_atual"]  # Usa o diretório atual
    directory_path = os.path.join(user_directory, directory).replace("\\", "/")

    print(f"Diretório que está sendo listado: {directory_path}")  # Para depuração

    if not directory_path.startswith(user_directory):  # Impede o acesso a diretórios fora do diretório do usuário
        print("Erro: Você não tem permissão para acessar esse diretório.")
        return

    # Verifica se o diretório existe
    if not os.path.exists(directory_path):
        print(f"Erro: Diretório '{directory_path}' não encontrado.")
        return
    
    # Lista os arquivos e diretórios no diretório
    files = os.listdir(directory_path)
    print(f"Conteúdo de {directory_path}:")
    for f in files:
        print(f"- {f}")

def change_directory(directory, user):
    """Altera o diretório de trabalho do usuário"""
    # Obtém o caminho completo para o diretório desejado dentro do diretório do usuário
    user_directory = user["diretorio"]
    target_directory = os.path.join(user_directory, directory).replace("\\", "/")

    # Verifica se o diretório existe
    if not os.path.exists(target_directory):
        print(f"Erro: O diretório '{directory}' não existe.")
        return

    # Verifica se o diretório é acessível
    if not os.path.isdir(target_directory):
        print(f"Erro: '{directory}' não é um diretório válido.")
        return

    # Atualiza o diretório de trabalho do usuário
    user["diretorio_atual"] = target_directory
    print(f"Diretório alterado para: {target_directory}")

def create_file(filepath, user):
    ensure_base_directory()  # Garantir que o diretório base existe

    # Garante que o arquivo está dentro do diretório do usuário
    filepath = os.path.join(user["diretorio"], filepath)
    directory = os.path.dirname(filepath)

    if not os.path.exists(directory):
        os.makedirs(directory)  # Cria o diretório se não existir
    
    with open(filepath, "w") as f:
        f.write("Conteúdo aleatório")
    
    print(f"Arquivo '{filepath}' criado com sucesso!")

def create_directory(directory, user):
    """Cria um diretório dentro do diretório específico do usuário"""
    if not isinstance(user, dict):
        print("Erro: Usuário não encontrado.")
        return

    # Verifica se o nome do diretório está correto
    if not directory:
        print("Erro: Nome do diretório não pode ser vazio.")
        return

    # Cria o caminho completo do diretório, dentro do diretório do usuário
    user_directory = user["diretorio"]
    directory_path = os.path.join(user_directory, directory)
    
    # Cria o diretório caso não exista
    try:
        os.makedirs(directory_path, exist_ok=True)
        print(f"Diretório '{directory}' criado com sucesso em {directory_path}!")
    except Exception as e:
        print(f"Erro ao criar diretório: {e}")


def delete_file(filepath, user):
    # Garante que o arquivo está dentro do diretório do usuário
    filepath = os.path.join(user["diretorio"], filepath)
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Arquivo '{filepath}' não encontrado.")
    
    os.remove(filepath)
    print(f"Arquivo '{filepath}' apagado com sucesso!")

def delete_directory(directory, user, force=False):
    # Garante que o diretório está dentro do diretório do usuário
    directory_path = os.path.join(user["diretorio"], directory)
    
    if not os.path.exists(directory_path):
        raise FileNotFoundError(f"Diretório '{directory_path}' não encontrado.")

    # Verifica se o diretório está vazio
    if len(os.listdir(directory_path)) > 0:
        print(f"Não é possível apagar o diretório '{directory_path}' porque ele não está vazio.")
        return
    
    # Se não for necessário forçar, usa os.rmdir() para apagar apenas diretórios vazios
    if force:
        shutil.rmtree(directory_path)
        print(f"Diretório '{directory_path}' apagado com força!")
    else:
        os.rmdir(directory_path)
        print(f"Diretório '{directory_path}' apagado com sucesso!")

def clear_screen():
    """Limpa a tela do terminal"""
    if os.name == 'nt':  # Verifica se o sistema operacional é Windows
        os.system('cls')  # Comando para limpar a tela no Windows
    else:
        os.system('clear')  # Comando para limpar a tela em sistemas Unix (Linux, Mac)

def exit_shell():
    print("Saindo do MiniShell. Até logo!")
    exit()  # Encerra o programa
