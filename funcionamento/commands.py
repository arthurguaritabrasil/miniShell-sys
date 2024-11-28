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
            force = "--force" in parts
            return delete_directory(directory=parts[2], user=user)

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
    """Cria um arquivo e associa o dono a ele."""
    # Diretório do usuário
    user_directory = user["diretorio_atual"]
    
    # Caminho do novo arquivo
    file_path = os.path.join(user_directory, file_name)
    
    # Cria o arquivo
    try:
        with open(file_path, 'w') as f:
            f.write('')  # Cria um arquivo vazio
        print(f"Arquivo '{file_name}' criado com sucesso!")

        # Salva o dono do arquivo
        file_metadata = {"dono": user["nome"]}
        file_metadata_path = file_path + '.meta'  # Armazenamos as metainformações em um arquivo '.meta'
        with open(file_metadata_path, 'w') as meta_file:
            json.dump(file_metadata, meta_file)

    except Exception as e:
        print(f"Erro ao criar o arquivo: {e}")

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
    # Gera o caminho absoluto do arquivo
    absolute_file_path = os.path.join(user["diretorio_atual"], file_path)
    print(f"Diretório atual do usuário: {user['diretorio_atual']}")
    print(f"Caminho absoluto do arquivo a ser deletado: {absolute_file_path}")
    
    if absolute_file_path.startswith(user["diretorio_atual"]):
        try:
            os.remove(absolute_file_path)
            print(f"Arquivo '{absolute_file_path}' excluído com sucesso!")
        except FileNotFoundError:
            print(f"Erro: Arquivo '{absolute_file_path}' não encontrado.")
    else:
        print("Erro: O arquivo não está dentro do diretório do usuário.")

def delete_directory(directory, user, force=False):
    """Remove um diretório, verificando permissões e podendo forçar a remoção."""
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

    # Verifica se o usuário tem permissão para excluir o diretório
    if not force:
        if os.path.exists(metadata_path):
            try:
                # Verifica se o arquivo de metadados não está vazio
                with open(metadata_path, 'r') as f:
                    content = f.read().strip()  # Remove espaços em branco
                    if not content:
                        print(f"Erro: O arquivo de metadados '{metadata_path}' está vazio.")
                        return
                    
                    metadata = json.loads(content)
                    
                    # Verifica se o dono do diretório é o usuário
                    if metadata.get("dono") != user["nome"]:
                        print("Erro: Você não tem permissão para excluir este diretório.")
                        return

            except json.JSONDecodeError:
                print(f"Erro: O arquivo de metadados '{metadata_path}' está corrompido.")
                return

    # Exclui o diretório
    try:
        shutil.rmtree(target_directory)  # Apaga o diretório e seu conteúdo
        if os.path.exists(metadata_path):
            os.remove(metadata_path)  # Remove o arquivo de metadados associado
        print(f"Diretório '{directory}' removido com sucesso!")
    except Exception as e:
        print(f"Erro ao remover o diretório: {e}")

def clear_screen():
    """Limpa a tela do terminal"""
    if os.name == 'nt':  # Verifica se o sistema operacional é Windows
        os.system('cls')  # Comando para limpar a tela no Windows
    else:
        os.system('clear')  # Comando para limpar a tela em sistemas Unix (Linux, Mac)

def exit_shell():
    print("Saindo do MiniShell. Até logo!")
    exit()  # Encerra o programa
