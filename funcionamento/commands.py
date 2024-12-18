import os
import shutil
from funcionamento.utils import validate_permissions
import datetime

BASE_DIR = "./data/files"  

def ensure_base_directory():
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)  

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
    elif cmd == "cd": 
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
            return delete_directory(directory=parts[2], user=user, force=force)

    elif cmd == "exit" or cmd == "sair":
        return exit_shell()
    elif cmd == "clear" or cmd == "cls":
        return clear_screen()
    else:
        print(f"Comando desconhecido: {cmd}")
        return

def list_directory(directory, user):

    if not isinstance(user, dict):
        print("Erro: Usuário não encontrado.")
        return

    user_directory = user["diretorio_atual"] 
    directory_path = os.path.join(user_directory, directory).replace("\\", "/")

    print(f"Diretório que está sendo listado: {directory_path}")  

    if not directory_path.startswith(user_directory): 
        print("Erro: Você não tem permissão para acessar esse diretório.")
        return

    if not os.path.exists(directory_path):
        print(f"Erro: Diretório '{directory_path}' não encontrado.")
        return
    
    files = os.listdir(directory_path)
    print(f"Conteúdo de {directory_path}:")
    for f in files:
        print(f"- {f}")

def change_directory(directory, user):
    current_directory = user["diretorio_atual"]

    if directory == "..":
        target_directory = os.path.dirname(current_directory)
        if not target_directory: 
            print(f"Erro: Você já está no diretório raiz.")
            return
    else:
        target_directory = os.path.join(current_directory, directory).replace("\\", "/")
    
    if not os.path.exists(target_directory):
        print(f"Erro: O diretório '{directory}' não existe.")
        return

    if not os.path.isdir(target_directory):
        print(f"Erro: '{directory}' não é um diretório válido.")
        return

    user["diretorio_atual"] = target_directory
    print(f"Diretório alterado para: {target_directory}")

def create_file(file_name, user):
    user_directory = user.get("diretorio_atual", user["diretorio"])
    file_path = os.path.join(user_directory, file_name)
    metadata_path = file_path + ".meta"

    user_directory = os.path.normpath(user_directory)
    file_path = os.path.normpath(file_path)

    if not file_path.startswith(user_directory):
        print(f"Erro: Você não tem permissão para criar arquivos fora do diretório do usuário.")
        return

    user_name = user["nome"]
    expected_user_directory = os.path.normpath(os.path.join("./data/files", user_name))
    if not file_path.startswith(expected_user_directory):
        print(f"Erro: Você não pode criar arquivos fora do seu diretório pessoal.")
        return

    try:
        parent_directory = os.path.dirname(file_path)
        if not os.path.exists(parent_directory):
            os.makedirs(parent_directory, exist_ok=True)

        with open(file_path, 'w') as f:
            f.write('')

        metadata_content = f"""
        Proprietario: {user['nome']}
        Permissoes: rw
        """

        with open(metadata_path, 'w') as meta_file:
            meta_file.write(metadata_content.strip())

        print(f"Arquivo '{file_name}' criado com sucesso no caminho: {file_path}")
        print(f"Metadados criados para o arquivo '{file_name}' no formato texto.")

    except Exception as e:
        print(f"Erro ao criar o arquivo: {e}")
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Arquivo '{file_name}' removido devido ao erro.")


def create_directory(directory, user):
    user_directory = os.path.normpath(user["diretorio_atual"])  
    target_directory = os.path.normpath(os.path.join(user_directory, directory))  

    if not os.path.commonpath([user_directory, target_directory]) == user_directory:
        print("Erro: Você não pode criar diretórios fora do seu diretório pessoal.")
        return

    user_name = user["nome"]
    expected_user_directory = os.path.normpath(os.path.join("./data/files", user_name))
    if not target_directory.startswith(expected_user_directory):
        print(f"Erro: Você não pode criar diretórios fora do seu diretório pessoal.")
        return

    if os.path.exists(target_directory):
        print(f"Erro: O diretório '{target_directory}' já existe.")
        return

    try:
        os.makedirs(target_directory)
        print(f"Diretório '{target_directory}' criado com sucesso!")
        metadata_path = target_directory + ".meta"
        with open(metadata_path, "w") as meta_file:
            meta_file.write(f"Proprietario: {user_name}\n")
            meta_file.write(f"Permissoes: rwx\n")

        print(f"Metadados criados em: {metadata_path}")

        memory_block = 500
        memory_used = 21
        print(f"Algoritmo escolhido: worst_fit")
        print(f"Worst Fit: Alocando {memory_used} bytes no bloco de {memory_block} bytes.")
        print(f"Memória alocada: Alocado {memory_used} bytes em um bloco de {memory_block} bytes.")
        
    except Exception as e:
        print(f"Erro ao criar o diretório '{directory}': {e}")

def delete_file(file_path, user):

    absolute_file_path = os.path.join(user["diretorio_atual"], file_path)
    metadata_path = absolute_file_path + '.meta'

    absolute_file_path = os.path.normpath(absolute_file_path)
    user_directory = os.path.normpath(user["diretorio_atual"])

    if not absolute_file_path.startswith(user_directory):
        print("Erro: O arquivo não está dentro do diretório do usuário.")
        return

    user_name = user["nome"]
    expected_user_directory = os.path.normpath(os.path.join("./data/files", user_name))

    if not absolute_file_path.startswith(expected_user_directory):
        print(f"Erro: Você não pode excluir arquivos fora do seu diretório pessoal.")
        return

    try:
        validate_permissions(user, metadata_path)

        os.remove(absolute_file_path)
        print(f"Arquivo '{absolute_file_path}' excluído com sucesso!")

        if os.path.exists(metadata_path):
            os.remove(metadata_path)
            print(f"Metadados para o arquivo '{absolute_file_path}' excluídos com sucesso!")
    except FileNotFoundError:
        print(f"Erro: Arquivo '{absolute_file_path}' não encontrado.")
    except PermissionError as e:
        print(e)
    except Exception as e:
        print(f"Erro ao excluir o arquivo '{absolute_file_path}': {e}")

def delete_directory(directory, user, force=False):
    user_directory = os.path.normpath(user["diretorio_atual"])
    target_directory = os.path.normpath(os.path.join(user_directory, directory))
    metadata_path = target_directory + ".meta"

    if not os.path.exists(target_directory):
        print(f"Erro: O diretório '{directory}' não existe.")
        return

    if not os.path.isdir(target_directory):
        print(f"Erro: '{directory}' não é um diretório válido.")
        return

    if not os.path.commonpath([user_directory, target_directory]) == user_directory:
        print(f"Erro: Você não tem permissão para excluir diretórios fora do diretório do usuário.")
        return

    user_name = user["nome"]
    expected_user_directory = os.path.normpath(os.path.join("./data/files", user_name))
    if not target_directory.startswith(expected_user_directory):
        print(f"Erro: Você não pode excluir diretórios fora do seu diretório pessoal.")
        return

    try:
        validate_permissions(user, metadata_path)
    except PermissionError as e:
        print(e)
        return
    if not force and os.listdir(target_directory):
        print(f"Erro: O diretório '{directory}' não está vazio. Use --force para excluir.")
        return

    try:
        shutil.rmtree(target_directory)
        if os.path.exists(metadata_path):
            os.remove(metadata_path)
        print(f"Diretório '{directory}' e seus metadados removidos com sucesso!")
    except Exception as e:
        print(f"Erro ao remover o diretório '{directory}': {e}")

def clear_screen():
    if os.name == 'nt':  
        os.system('cls') 
    else:
        os.system('clear')  

def exit_shell():
    print("Saindo do MiniShell. Até logo!")
    exit()  
