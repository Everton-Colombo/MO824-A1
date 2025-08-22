# Solucionador para o Problema de Cobertura Máxima com Função Objetivo Quadrática (Max--SC-QBF)

Este projeto contém um conjunto de scripts em Python para gerar, modelar e resolver instâncias do Problema de Cobertura Máxima com uma Função Objetivo Booleana Quadrática (Max-SC-QBF). A modelagem matemática é implementada utilizando a biblioteca Pyomo, e o Gurobi é utilizado como solucionador.

## Estrutura do Projeto

```
.
├── data
│   └── instances
│       ├── gen1/       # Instâncias do Gerador 1
│       ├── gen2/       # Instâncias do Gerador 2
│       └── gen3/       # Instâncias do Gerador 3
├── logs
│   ├── gen1/           # Logs do Gurobi para o Gerador 1
│   ├── gen2/           # Logs do Gurobi para o Gerador 2
│   └── gen3/           # Logs do Gurobi para o Gerador 3
├── instance_gen1.py    # Script para gerar instâncias básicas
├── instance_gen2.py    # Script para gerar instâncias com subconjuntos grandes
├── instance_gen3.py    # Script para gerar instâncias com coeficientes não-negativos
├── experiments.py      # Script principal para executar os experimentos
├── instance_io.py      # Funções para leitura e escrita de instâncias
├── instance_solver.py  # Funções para modelagem e solução
└── test.ipynb          # Notebook com exemplos de uso das funções
```

## Pré-requisitos

Para executar este projeto, você precisará ter o Python 3 e as seguintes bibliotecas instaladas. É fundamental que o otimizador Gurobi esteja instalado e com uma licença ativa.

- **Python 3:** [Instruções de instalação](https://www.python.org/)
- **Pyomo:**
  ```bash
  pip install pyomo
  ```
- **Gurobi:** O código utiliza o `SolverFactory('gurobi')` do Pyomo para se conectar ao solucionador. Certifique-se de que o Gurobi está corretamente instalado em seu sistema.
  - [Download e instalação do Gurobi](https://www.gurobi.com/downloads/gurobi-software/)

## Como Usar

O fluxo de trabalho é dividido em duas etapas principais: primeiro, a geração das instâncias de teste e, em segundo, a execução dos experimentos para resolvê-las.

### 1. Geração de Instâncias

Três scripts estão disponíveis para gerar diferentes classes de instâncias. Os arquivos `.txt` resultantes são salvos automaticamente nos subdiretórios `data/instances/gen*`.

- **Gerador 1: Básico**
  Cria instâncias com parâmetros gerais e coeficientes da função objetivo variando entre -10 e 10.
  ```bash
  # Sintaxe: python instance_gen1.py <numero_de_instancias>
  # Exemplo para criar 5 instâncias:
  python instance_gen1.py 5
  ```

- **Gerador 2: Subconjuntos Grandes**
  Cria instâncias onde os subconjuntos de cobertura possuem um tamanho mínimo garantido, proporcional ao tamanho do universo.
  ```bash
  # Sintaxe: python instance_gen2.py <numero_de_instancias> <tamanho_min_subconjunto>
  # Exemplo para criar 5 instâncias com subconjuntos de tamanho >= 0.8*n:
  python instance_gen2.py 5 0.8
  ```

- **Gerador 3: Coeficientes Não-Negativos**
  Cria instâncias onde uma porcentagem definida dos coeficientes da função objetivo ($a_{ij}$) é não-negativa.
  ```bash
  # Sintaxe: python instance_gen3.py <numero_de_instancias> <porcentagem_nao_negativos>
  # Exemplo para criar 5 instâncias com 80% dos coeficientes não-negativos:
  python instance_gen3.py 5 0.8
  ```

### 2. Executando os Experimentos

Após gerar as instâncias, o script `experiments.py` automatiza o processo de solução. Ele varre os subdiretórios em `data/instances/`, resolve cada instância encontrada e armazena os resultados.

Para executar, simplesmente rode o script:
```bash
python experiments.py
```

O script irá gerar os seguintes artefatos:
- **Logs de Resumo (`summary_results*.log`):** Na raiz do projeto, um arquivo de log para cada tipo de gerador, contendo os resultados consolidados (valor da função objetivo, tempo de solução, etc.).
- **Logs do Solucionador (`logs/`):** Um log detalhado da execução do Gurobi para cada instância individual, organizado em subpastas correspondentes.

### Exemplo de Uso e Testes

O Jupyter Notebook `test.ipynb` serve como um guia detalhado e interativo. Ele demonstra passo a passo como usar as funções principais do projeto para:
- Ler um arquivo de instância.
- Construir o modelo de otimização em Pyomo.
- Resolver uma única instância e inspecionar os resultados.
