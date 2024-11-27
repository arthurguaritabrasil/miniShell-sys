import os
import random
from funcionamento.utils import allocate_memory, deallocate_memory
from funcionamento.commands import execute_command  # Importação corrigida

class ProcessManager:
    def __init__(self):
        self.processes = {}

    def create_process(self, command):
        pid = random.randint(1000, 9999)
        self.processes[pid] = {
            "command": command,
            "allocated_memory": allocate_memory(len(command))  # Simulação simples
        }
        print(f"Processo criado com PID {pid}.")
        return pid

    def execute_process(self, pid, user):
        if pid not in self.processes:
            raise ValueError(f"Processo com PID {pid} não encontrado.")
        
        command = self.processes[pid]["command"]
        execute_command(command, user)  # Executa o comando usando o método importado
        print(f"Comando '{command}' executado com sucesso!")

        # Liberação de memória
        deallocate_memory(self.processes[pid]["allocated_memory"])
        del self.processes[pid]
