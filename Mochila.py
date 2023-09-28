import random

# Definindo os parâmetros do problema
pesos = [2, 3, 4, 5, 9]  # Pesos dos livros
valores = [3, 4, 8, 8, 10]  # Preço dos livros
capacidade_mochila = 20
tamanho_populacao = 10  # Número de indivíduos (cromossomos) por população
taxa_mutacao = 0.1
geracoes = 100


# Função de fitness (adaptabilidade)
def fitness(cromossomo):
    soma_pesos = sum(pesos[i] for i in range(len(cromossomo)) if cromossomo[i])
    soma_valores = sum(valores[i] for i in range(len(cromossomo)) if cromossomo[i])
    if soma_pesos > capacidade_mochila:
        return 0
    else:
        return soma_valores


# Função de crossover (cruzamento)
def crossover(pai1, pai2):
    ponto_corte = random.randint(1, len(pai1)-1)
    filho1 = pai1[:ponto_corte] + pai2[ponto_corte:]
    filho2 = pai2[:ponto_corte] + pai1[ponto_corte:]
    return filho1, filho2


# Função de mutação
def mutacao(individuo):
    posicao = random.randint(0, len(individuo)-1)
    individuo[posicao] = not individuo[posicao]
    return individuo


# Inicializando a população
populacao = [[random.choice([0, 1]) for _ in range(len(pesos))] for _ in range(tamanho_populacao)]

# Algoritmo genético
for geracao in range(geracoes):
    populacao = sorted(populacao, key=lambda x: fitness(x), reverse=True)
    nova_populacao = []

    # Elitismo: mantém os melhores indivíduos
    nova_populacao.extend(populacao[:2])

    # Geração de novos indivíduos através de crossover e mutação
    for _ in range(tamanho_populacao // 2):
        pai1, pai2 = random.choice(populacao[:5]), random.choice(populacao[:5])
        filho1, filho2 = crossover(pai1, pai2)
        if random.random() < taxa_mutacao:
            filho1 = mutacao(filho1)
        if random.random() < taxa_mutacao:
            filho2 = mutacao(filho2)
        nova_populacao.extend([filho1, filho2])

    populacao = nova_populacao

# Obtendo o melhor indivíduo após as gerações
melhor_individuo = max(populacao, key=fitness)
melhor_individuo = [1 if gene else 0 for gene in melhor_individuo]

# Exibindo resultados
print("Melhor Indivíduo:", melhor_individuo)
print("Valor Total:", sum(valores[i] for i in range(len(melhor_individuo)) if melhor_individuo[i]))
print("Peso Total:", sum(pesos[i] for i in range(len(melhor_individuo)) if melhor_individuo[i]))
