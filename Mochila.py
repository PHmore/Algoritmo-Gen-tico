from PySimpleGUI import PySimpleGUI as sg
import random


def converter_int(string):
    lista_inteira = list()
    string = string.split(" ")

    for item in string:
        lista_inteira.append(int(item))

    return lista_inteira


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


# Layout de janelas
tela_parametros = [
    [sg.Text('Pesos dos livros:'), sg.Push(), sg.Input(key='pesos')],
    [sg.Text('Valores dos livros:'), sg.Push(), sg.Input(key='valores')],
    [sg.Text('Capacidade da mochila:'), sg.Input('', (5, 1), key='capacidade_mochila')],
    [sg.Text('Tamanho da população:'), sg.Input('', (5, 1), key='tamanho_populacao')],
    [sg.Text('Taxa de mutação:'), sg.Input('', (5, 1), key='taxa_mutacao')],
    [sg.Text('Número de gerações:'), sg.Input('', (5, 1), key='geracoes')],
    [sg.Push(), sg.Button('continuar'), sg.Push(), sg.Button('cancelar'), sg.Push()]
]

# Definindo os parâmetros do problema
pesos = list()
valores = list()
capacidade_mochila = 1
tamanho_populacao = 1  # Número de indivíduos (cromossomos) por população
taxa_mutacao = 0.1
geracoes = 1

janela_parametros = sg.Window('ALGORITMO GENÉTICO', layout=tela_parametros)
while True:
    e, v = janela_parametros.read()

    if e == sg.WINDOW_CLOSED:
        break
    if e == 'cancelar':
        janela_parametros.close()
        break
    if e == 'continuar':
        pesos = v['pesos'][:]
        valores = v['valores'][:]
        capacidade_mochila = int(v['capacidade_mochila'])
        tamanho_populacao = int(v['tamanho_populacao'])
        taxa_mutacao = float(v['taxa_mutacao'])
        geracoes = int(v['geracoes'])
        janela_parametros.close()
        break

pesos = converter_int(pesos)
valores = converter_int(valores)

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
        valor_total += valores[c]
        peso_total += pesos[c]

# Exibindo resultados
print("Melhor Indivíduo:", melhor_cromossomo)
print("Valor Total:", valor_total)
print("Peso Total:", peso_total)
