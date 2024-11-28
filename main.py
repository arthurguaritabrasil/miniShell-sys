"""

Arthur Guaritá Brasil - 22303654
Link GitHub: https://github.com/arthurguaritabrasil/miniShell-sys

"""

from funcionamento.auth import create_or_login_user
from funcionamento.process_manager import ProcessManager

def main():
    # Chama a função que irá decidir entre login ou criar um novo usuário
    user = create_or_login_user()  # user agora é um dicionário com as informações do usuário logado
    
    if not user:
        print("Falha ao fazer login ou criar um usuário.")
        return  # Se o usuário não foi autenticado ou criado, encerra a execução
    
    # Cria uma instância do process manager
    process_manager = ProcessManager()

    while True:
        # Recebe o comando do usuário
        command = input("\nMiniSO> ").strip()
        print("")
        
        if command.lower() == "sair":
            break

        # Cria o processo e executa com as informações do usuário (o dicionário user)
        pid = process_manager.create_process(command)
        process_manager.execute_process(pid, user)  # Passando o dicionário user

if __name__ == "__main__":
    main()
