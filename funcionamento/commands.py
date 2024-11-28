import os
import shutil
from funcionamento.utils import validate_permissions
import json

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
            force = "--force" in parts  # Verifica se '--force' está no comando
            return delete_directory(directory=parts[2], user=user, force=force)

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
    # Obtém o diretório atual do usuário
    current_directory = user["diretorio_atual"]

    # Se o diretório for '..', navega para o diretório pai
    if directory == "..":
        # Obtém o diretório pai
        target_directory = os.path.dirname(current_directory)
        if not target_directory:  # Verifica se já está no diretório raiz
            print(f"Erro: Você já está no diretório raiz.")
            return
    else:
        # Concatena o caminho do diretório desejado
        target_directory = os.path.join(current_directory, directory).replace("\\", "/")
    
    # Verifica se o diretório existe
    if not os.path.exists(target_directory):
        print(f"Erro: O diretório '{directory}' não existe.")
        return

    # Verifica se é um diretório válido
    if not os.path.isdir(target_directory):
        print(f"Erro: '{directory}' não é um diretório válido.")
        return

    # Atualiza o diretório atual do usuário
    user["diretorio_atual"] = target_directory
    print(f"Diretório alterado para: {target_directory}")

def create_file(file_name, user):
    """
    Cria um arquivo e associa o dono a ele.
    """
    # Diretório atual do usuário
    user_directory = user.get("diretorio_atual", user["diretorio"])
    
    # Caminho completo para o novo arquivo
    file_path = os.path.join(user_directory, file_name)
    metadata_path = file_path + '.meta'  # Caminho do arquivo de metadados

    try:
        # Obtém o diretório pai do arquivo
        parent_directory = os.path.dirname(file_path)
        
        # Garante que o diretório pai existe
        os.makedirs(parent_directory, exist_ok=True)

        # Criação do arquivo vazio
        with open(file_path, 'w') as f:
            f.write('')  # Cria um arquivo vazio
        print(f"Arquivo '{file_name}' criado com sucesso no caminho: {file_path}")

        # Criação do arquivo de metadados
        file_metadata = {
            "dono": user["nome"],  # Nome do usuário que criou o arquivo
            "permissoes": "rw",  # Permissões padrão para leitura e escrita
        }
        with open(metadata_path, 'w') as meta_file:
            json.dump(file_metadata, meta_file)
        print(f"Metadados criados para o arquivo '{file_name}' em: {metadata_path}")

    except PermissionError as e:
        print(f"Erro: Permissões insuficientes para criar o arquivo '{file_name}'.")
    except Exception as e:
        print(f"Erro ao criar o arquivo '{file_name}': {e}")

def create_directory(directory, user):
    """Cria um novo diretório e gera o arquivo de metadados com o dono."""
    user_directory = user["diretorio_atual"]
    target_directory = os.path.join(user_directory, directory)
    metadata_path = target_directory + ".meta"

    # Verifica se o diretório já existe
    if os.path.exists(target_directory):
        print(f"Erro: O diretório '{directory}' já existe.")
        return

    try:
        # Cria o diretório
        os.makedirs(target_directory)

        # Cria o arquivo de metadados
        metadata = {
            "dono": user["nome"],  # O nome do usuário que criou o diretório
            "permissoes": "rw"  # Permissões de leitura e escrita, por exemplo
        }

        # Grava os metadados no arquivo
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f)

        print(f"Diretório '{directory}' criado com sucesso!")
    
    except Exception as e:
        print(f"Erro ao criar o diretório: {e}")

def delete_file(file_path, user):
    """Remove um arquivo e seus metadados."""
    # Gera o caminho absoluto do arquivo
    absolute_file_path = os.path.join(user["diretorio_atual"], file_path)
    metadata_path = absolute_file_path + '.meta'  # Caminho do arquivo de metadados

    if absolute_file_path.startswith(user["diretorio_atual"]):
        try:
            # Remove o arquivo
            os.remove(absolute_file_path)
            print(f"Arquivo '{absolute_file_path}' excluído com sucesso!")

            # Remove o arquivo de metadados, se existir
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
    """Remove um diretório e seus metadados associados."""
    user_directory = user["diretorio_atual"]
    target_directory = os.path.join(user_directory, directory)
    metadata_path = target_directory + ".meta"  # Caminho do arquivo de metadados

    # Verifica se o diretório existe
    if not os.path.exists(target_directory):
        print(f"Erro: O diretório '{directory}' não existe.")
        return

    # Verifica se o diretório é acessível
    if not os.path.isdir(target_directory):
        print(f"Erro: '{directory}' não é um diretório válido.")
        return

    # Se não for 'force', verifica se o diretório está vazio
    if not force:
        if os.listdir(target_directory):  # Se o diretório não estiver vazio
            print(f"Erro: O diretório '{directory}' não está vazio. Use --force para excluir.")
            return

    # Verifica permissões do usuário para excluir o diretório
    if not force:
        if os.path.exists(metadata_path):
            try:
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)
                    # Verifica se o usuário é o dono do diretório
                    if metadata.get("dono") != user["nome"]:
                        print("Erro: Você não tem permissão para excluir este diretório.")
                        return
            except json.JSONDecodeError:
                print(f"Erro: O arquivo de metadados '{metadata_path}' está corrompido.")
                return

    # Exclui o diretório e os metadados associados
    try:
        shutil.rmtree(target_directory)  # Apaga o diretório e seu conteúdo
        if os.path.exists(metadata_path):
            os.remove(metadata_path)  # Remove o arquivo de metadados associado
        print(f"Diretório '{directory}' e seus metadados removidos com sucesso!")
    except Exception as e:
        print(f"Erro ao remover o diretório '{directory}': {e}")

def clear_screen():
    """Limpa a tela do terminal"""
    if os.name == 'nt':  # Verifica se o sistema operacional é Windows
        os.system('cls')  # Comando para limpar a tela no Windows
    else:
        os.system('clear')  # Comando para limpar a tela em sistemas Unix (Linux, Mac)

def exit_shell():
    print("Saindo do MiniShell. Até logo!")
    exit()  # Encerra o programa
