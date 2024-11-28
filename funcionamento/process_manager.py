import random
from funcionamento.fitsMemory import allocate_memory, deallocate_memory
from funcionamento.commands import execute_command

class ProcessManager:
    def __init__(self):
        self.processes = {}

    def create_process(self, command):
        pid = random.randint(1000, 9999)
        self.processes[pid] = {
            "command": command,
            "allocated_memory": None  
        }
        print(f"Processo criado com PID {pid}.\n")
        return pid

    def execute_process(self, pid, user):
        if pid not in self.processes:
            raise ValueError(f"Processo com PID {pid} não encontrado.")
        
        command = self.processes[pid]["command"]
        
        allocated_memory = allocate_memory(len(command))  
        self.processes[pid]["allocated_memory"] = allocated_memory 
        print(f"Memória alocada: {allocated_memory}")

        valid_commands = ["ls", "cd", "apagar", "criar", "clear", "cls", "exit", "listar"] 
        if command.split()[0] not in valid_commands:
            print(f"Erro: O comando '{command}' não é reconhecido.")
            deallocate_memory(self.processes[pid]["allocated_memory"])
            del self.processes[pid]
            return

        try:
            execute_command(command, user)
        except Exception as e:
            print(f"Erro ao executar o comando '{command}': {str(e)}")

        deallocate_memory(self.processes[pid]["allocated_memory"])
        del self.processes[pid]
