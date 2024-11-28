"""

Arthur Guaritá Brasil - 22303654
Link GitHub: https://github.com/arthurguaritabrasil/miniShell-sys

"""

from funcionamento.auth import create_or_login_user
from funcionamento.process_manager import ProcessManager

def main():
    user = create_or_login_user() 
    
    if not user:
        print("Falha ao fazer login ou criar um usuário.")
        return 
    
    process_manager = ProcessManager()

    while True:
        command = input("\nMiniSO> ").strip()
        print("")
        
        if command.lower() == "sair":
            break

        pid = process_manager.create_process(command)
        process_manager.execute_process(pid, user)

if __name__ == "__main__":
    main()
