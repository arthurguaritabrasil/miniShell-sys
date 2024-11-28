import random
from funcionamento.fitsMemory import allocate_memory, deallocate_memory
from funcionamento.commands import execute_command  # Certifique-se de que esta importação está correta

class ProcessManager:
    def __init__(self):
        self.processes = {}

    def create_process(self, command):
        pid = random.randint(1000, 9999)
        self.processes[pid] = {
            "command": command,
            "allocated_memory": None  # Inicializa como None
        }
        print(f"Processo criado com PID {pid}.\n")
        return pid

    def execute_process(self, pid, user):
        """Este método executa um processo com base no PID e no usuário"""
        if pid not in self.processes:
            raise ValueError(f"Processo com PID {pid} não encontrado.")
        
        command = self.processes[pid]["command"]
        
        # Alocação de memória
        allocated_memory = allocate_memory(len(command))  # Aloca a memória
        self.processes[pid]["allocated_memory"] = allocated_memory  # Armazena a memória alocada
        print(f"Memória alocada: {allocated_memory}")

        # Verifica se o comando é válido antes de executá-lo
        valid_commands = ["ls", "cd", "apagar", "criar", "clear", "cls", "exit", "listar"]  # Adicione seus comandos válidos aqui
        if command.split()[0] not in valid_commands:
            print(f"Erro: O comando '{command}' não é reconhecido.")
            # Libera a memória e exclui o processo sem tentar executá-lo
            deallocate_memory(self.processes[pid]["allocated_memory"])
            del self.processes[pid]
            return

        # Executa o comando
        execute_command(command, user)
        print(f"Comando '{command}' executado com sucesso!")

        # Liberação de memória após execução bem-sucedida
        deallocate_memory(self.processes[pid]["allocated_memory"])
        del self.processes[pid]
