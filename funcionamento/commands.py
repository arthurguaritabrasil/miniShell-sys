import os
import shutil
from funcionamento.utils import validate_permissions
import json

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
    metadata_path = file_path + '.meta'

    try:
        parent_directory = os.path.dirname(file_path)
  
        os.makedirs(parent_directory, exist_ok=True)

        with open(file_path, 'w') as f:
            f.write('') 
        print(f"Arquivo '{file_name}' criado com sucesso no caminho: {file_path}")

        file_metadata = {
            "dono": user["nome"],  
            "permissoes": "rw",  
        }
        with open(metadata_path, 'w') as meta_file:
            json.dump(file_metadata, meta_file)
        print(f"Metadados criados para o arquivo '{file_name}' em: {metadata_path}")

    except PermissionError as e:
        print(f"Erro: Permissões insuficientes para criar o arquivo '{file_name}'.")
    except Exception as e:
        print(f"Erro ao criar o arquivo '{file_name}': {e}")

def create_directory(directory, user):
    user_directory = user["diretorio_atual"]
    target_directory = os.path.join(user_directory, directory)
    metadata_path = target_directory + ".meta"

    if os.path.exists(target_directory):
        print(f"Erro: O diretório '{directory}' já existe.")
        return

    try:
        os.makedirs(target_directory)

        metadata = {
            "dono": user["nome"],
            "permissoes": "rw"
        }

        with open(metadata_path, 'w') as f:
            json.dump(metadata, f)

        print(f"Diretório '{directory}' criado com sucesso!")
    
    except Exception as e:
        print(f"Erro ao criar o diretório: {e}")

def delete_file(file_path, user):

    absolute_file_path = os.path.join(user["diretorio_atual"], file_path)
    metadata_path = absolute_file_path + '.meta'

    if absolute_file_path.startswith(user["diretorio_atual"]):
        try:
            os.remove(absolute_file_path)
            print(f"Arquivo '{absolute_file_path}' excluído com sucesso!")
            if os.path.exists(metadata_path):
                os.remove(metadata_path)
                print(f"Metadados para o arquivo '{absolute_file_path}' excluídos com sucesso!")
        except FileNotFoundError:
            print(f"Erro: Arquivo '{absolute_file_path}' não encontrado.")
        except Exception as e:
            print(f"Erro ao excluir o arquivo '{absolute_file_path}': {e}")
    else:
        print("Erro: O arquivo não está dentro do diretório do usuário.")

def delete_directory(directory, user, force=False):
    user_directory = user["diretorio_atual"]
    target_directory = os.path.join(user_directory, directory)
    metadata_path = target_directory + ".meta" 

    if not os.path.exists(target_directory):
        print(f"Erro: O diretório '{directory}' não existe.")
        return
    if not os.path.isdir(target_directory):
        print(f"Erro: '{directory}' não é um diretório válido.")
        return
    if not force:
        if os.listdir(target_directory): 
            print(f"Erro: O diretório '{directory}' não está vazio. Use --force para excluir.")
            return
    if not force:
        if os.path.exists(metadata_path):
            try:
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)
                    if metadata.get("dono") != user["nome"]:
                        print("Erro: Você não tem permissão para excluir este diretório.")
                        return
            except json.JSONDecodeError:
                print(f"Erro: O arquivo de metadados '{metadata_path}' está corrompido.")
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
