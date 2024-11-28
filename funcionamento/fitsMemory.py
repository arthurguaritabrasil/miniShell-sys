import random

# Simulação de memória com blocos de tamanhos aleatórios
memory_blocks = [50, 200, 100, 300, 150, 500, 250]  # Tamanhos dos blocos de memória disponíveis

def allocate_memory(size):
    """
    Aloca memória aleatoriamente utilizando um dos três algoritmos: 
    first_fit, best_fit ou worst_fit.
    
    Parâmetros:
    - size (int): O tamanho da memória necessária para o processo.
    
    Retorna:
    - Um objeto representando o bloco de memória alocado ou uma mensagem de erro.
    """
    # Lista de algoritmos disponíveis
    algorithms = ["first_fit", "best_fit", "worst_fit"]
    
    # Escolhe aleatoriamente um dos algoritmos
    chosen_algorithm = random.choice(algorithms)
    print(f"Algoritmo escolhido: {chosen_algorithm}")
    
    # Chama a função correspondente ao algoritmo escolhido
    if chosen_algorithm == "first_fit":
        return first_fit(size)
    elif chosen_algorithm == "best_fit":
        return best_fit(size)
    elif chosen_algorithm == "worst_fit":
        return worst_fit(size)
    else:
        return "Algoritmo de alocação desconhecido."

def first_fit(size):
    """Algoritmo First Fit"""
    for i, block in enumerate(memory_blocks):
        if block >= size:
            # Aloca o bloco e o "remove" da memória disponível
            memory_blocks[i] -= size
            print(f"First Fit: Alocando {size} bytes no bloco de {block} bytes.")
            return f"Alocado {size} bytes em um bloco de {block} bytes."
    return "Memória insuficiente."

def best_fit(size):
    """Algoritmo Best Fit"""
    best_index = -1
    min_diff = float('inf')
    
    for i, block in enumerate(memory_blocks):
        if block >= size and (block - size) < min_diff:
            min_diff = block - size
            best_index = i
    
    if best_index != -1:
        block = memory_blocks[best_index]
        memory_blocks[best_index] -= size
        print(f"Best Fit: Alocando {size} bytes no bloco de {block} bytes.")
        return f"Alocado {size} bytes em um bloco de {block} bytes."
    
    return "Memória insuficiente."

def worst_fit(size):
    """Algoritmo Worst Fit"""
    worst_index = -1
    max_diff = -1
    
    for i, block in enumerate(memory_blocks):
        if block >= size and (block - size) > max_diff:
            max_diff = block - size
            worst_index = i
    
    if worst_index != -1:
        block = memory_blocks[worst_index]
        memory_blocks[worst_index] -= size
        print(f"Worst Fit: Alocando {size} bytes no bloco de {block} bytes.")
        return f"Alocado {size} bytes em um bloco de {block} bytes."
    
    return "Memória insuficiente."

def deallocate_memory(memory):
    """
    Libera a memória, ou seja, "desfaz" a alocação.
    Aqui, a função assume que a memória está sendo liberada para o mesmo bloco.
    """
    size = int(memory.split()[1])  # Obtém o tamanho do bloco alocado da string
    # A memória é liberada, ou seja, o espaço é restaurado ao bloco original.
    memory_blocks.append(size)  # Em uma implementação real, você pode querer unir blocos se necessário.
    print(f"{memory} desalocado.")
