import random

# Simulação de memória com blocos de tamanhos aleatórios
memory_blocks = [50, 200, 100, 300, 150, 500, 250]  # Tamanhos dos blocos de memória disponíveis

def allocate_memory(size):
    algorithms = ["first_fit", "best_fit", "worst_fit"]
    chosen_algorithm = random.choice(algorithms)
    print(f"Algoritmo escolhido: {chosen_algorithm}")
    
    if chosen_algorithm == "first_fit":
        return first_fit(size)
    elif chosen_algorithm == "best_fit":
        return best_fit(size)
    elif chosen_algorithm == "worst_fit":
        return worst_fit(size)
    else:
        return "Algoritmo de alocação desconhecido."

def first_fit(size):
    for i, block in enumerate(memory_blocks):
        if block >= size:
            memory_blocks[i] -= size
            print(f"First Fit: Alocando {size} bytes no bloco de {block} bytes.")
            return f"Alocado {size} bytes em um bloco de {block} bytes."
    return "Memória insuficiente."

def best_fit(size):
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
    size = int(memory.split()[1]) 
    memory_blocks.append(size) 
    print(f"{memory} desalocado.")
