import sys, random, os

# Esta função gera 'n' subconjuntos de um universo {1, ..., n}.
# A lógica garante que cada elemento do universo seja coberto por pelo menos
# um subconjunto.
def gen_subsets(n):
    n_set = list(range(1,n+1)) # Universo
    subsets = [] # Lista de subconjuntos
    
    # Cria 'n' subconjuntos
    for _ in range(n):
        # Cada subconjunto terá um tamanho aleatório (obs.: tamanho 0 = conjunto vazio)
        subset_size = random.randint(0, n) 
        # Amostra 'subset_size' elementos do universo para formar o subconjunto.
        subsets.append(set(random.sample(n_set, subset_size)))
    
    # Para garantir que exista pelo menos uma cobertura
    for i in n_set:
        subsets[random.randint(0,n-1)].add(i)
        
    return subsets

# Esta função cria um arquivo de instância completo.
# O 'filename_suffix' é usado para numerar os arquivos (ex: instance1.txt).
def create_instance(filename_suffix):
    
    # Seleciona aleatoriamente o número de variáveis 'n' de uma lista de valores
    # pré-definidos, conforme solicitado na atividade.
    n = random.choice([25, 50, 100, 200, 400])
    
    base_dir = os.path.join(".", "data", "instances", "instances3")
    os.makedirs(base_dir, exist_ok=True)

    filename = os.path.join(base_dir, f"instance{filename_suffix}.txt")    
    # Abre o arquivo para escrita e escreve o valor de 'n' na primeira linha.
    with open(filename, "w") as file:
        file.write(str(n) + "\n")
        
    # Chama a função para gerar os subconjuntos de cobertura.
    subsets = gen_subsets(n)

    with open(filename, "a") as file:
        
        for subset in subsets:
            file.write(str(len(subset)) + " ")
        file.write("\n")
        
        for subset in subsets:
            for element in subset:
                file.write(str(element) + " ")
            file.write("\n")
        
        for i in range(n, 0, -1):
            for j in range(i):
                if random.random() <= num_positive_coeff: # Isso tem "num_positive_coeff" de chance de retornar True
                    file.write(str(round(random.uniform(0, 10.0), 2)) + " ")
                else:
                    file.write(str(round(random.uniform(-10, 0), 2)) + " ")
                # Escolhi gerar floats entre -10 e 10
                # Há probabilidade "num_positive_coeff" de cadda um ser não-negativo
            file.write("\n")
            
        
# --- Bloco de Execução Principal ---

# Obtém o número de instâncias a serem criadas a partir do primeiro argumento
# Obtém a porcentagem de aij>=0 a partir do segundo argumento
# da linha de comando. Ex: 'python seu_script.py 5 0.8' criará 5 instâncias nas 
# quais 80% dos coeficientes da função objetivo são não-negativos.

num_instances = int(sys.argv[1])
num_positive_coeff = float(sys.argv[2]) #porcentagem de aij que são não-negativos (na verdade, probabilidade de cada aij ser não-negativo)

# Laço para chamar a função 'create_instance' o número de vezes especificado.
for instance in range(1, num_instances+1):
    create_instance(instance)
    
