import random

# Definindo os parâmetros do problema
pesos = [2, 3, 4, 5, 9]  # Pesos dos livros
valores = [3, 4, 8, 8, 10]  # Preço dos livros
capacidade_mochila = 20
tamanho_populacao = 6  # Número de indivíduos (cromossomos) por população
taxa_mutacao = 0.1
geracoes = 100


# Função de fitness (adaptabilidade)
def fitness(cromossomo):
    soma_pesos = soma_valores = 0
    for d in range(len(cromossomo)):
        if cromossomo[d] == 1:
            soma_pesos += pesos[d]
            soma_valores += valores[d]

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

    # Mantém os melhores cromossomos
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

# Obtendo o melhor cromossomo após as gerações
melhor_cromossomo = max(populacao, key=fitness)
melhor_cromossomo = [1 if gene else 0 for gene in melhor_cromossomo]

# Cálculo do total de peso e valor dos livros selecionados geneticamente
valor_total = peso_total = 0
for c in range(len(melhor_cromossomo)):
    if melhor_cromossomo[c] == 1:
        valor_total +=valores[c]
        peso_total += pesos[c]

# Exibindo resultados
print(f"Melhor Indivíduo: {melhor_cromossomo}")
print(f"Valor Total: {valor_total}")
print(f"Peso Total: {peso_total}")

