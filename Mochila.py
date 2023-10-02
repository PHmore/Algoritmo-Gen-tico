from PySimpleGUI import PySimpleGUI as sg
import random

sg.theme('Reddit')


def converter_int(string):  # Converte os elementos que foram lidos como string na interface em uma lista de inteiros

    '''
    Converte um inteiro
    '''

    lista_inteira = list()
    if ',' in string:
        string = string.replace(',', ' ')
    string = string.split(" ")

    for item in string:
        lista_inteira.append(int(item))

    print(lista_inteira)
    return lista_inteira


# Função onde recebe o cromossomo ler os genes e retorna o FITNESS
def fitness(cromossomo):

    '''
    Converte um inteiro
    '''

    soma_pesos = soma_valores = 0
    for d in range(len(cromossomo)):
        print (d)
        print (cromossomo)
        print (pesos)
        if cromossomo[d] == 1:
            soma_pesos += pesos[d]
            soma_valores += valores[d]

    if soma_pesos > capacidade_mochila:
        return 0
    else:
        return soma_valores


# Função de cruzamento genético
def crossover(pai1, pai2):

    '''
    Converte um inteiro
    '''

    ponto_corte = random.randint(1, len(pai1)-1)
    filho1 = pai1[:ponto_corte] + pai2[ponto_corte:]
    filho2 = pai2[:ponto_corte] + pai1[ponto_corte:]
    return filho1, filho2


# Função de mutação
def mutacao(individuo):

    '''
    Converte um inteiro
    '''

    posicao = random.randint(0, len(individuo)-1)
    individuo[posicao] = not individuo[posicao]
    return individuo


# Definição do layout da janela de inserção de dados
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

    if e == sg.WINDOW_CLOSED or e == 'cancelar':
        janela_parametros.close()
        exit()
    if e == 'continuar':
        pesos = v['pesos'][:]
        valores = v['valores'][:]
        capacidade_mochila = int(v['capacidade_mochila'])
        tamanho_populacao = int(v['tamanho_populacao'])
        taxa_mutacao = float(v['taxa_mutacao'])
        geracoes = int(v['geracoes'])
        janela_parametros.close()
        break

# Barra de progresso
tela_aguarde = [
    [sg.Text('Progresso')],
    [sg.ProgressBar(geracoes, orientation='h', size=(20, 20), key='progressbar')]
]

Carregamento = sg.Window('Barra de Progresso', tela_aguarde)

# Janela de histórico
log_layout = [
    [sg.Multiline(size=(60, 10), key='-LOG-', autoscroll=True)]
]

janela_logs = sg.Window('LOG', layout=log_layout)

log = []

pesos = converter_int(pesos)
valores = converter_int(valores)

# Inicializando a população
print(f'Printando pesos', pesos)
populacao = [[random.choice([0, 1]) for _ in range(len(pesos))] for _ in range(tamanho_populacao)]

# Algoritmo genético
for geracao in range(geracoes):
    log.append(f'populacao: {populacao} geracao: {geracao}')
    print(f'populacao: {populacao} geracao: {geracao}')

    event, values = Carregamento.read(timeout=1)  # Adiciona timeout para evitar bloqueio
    Carregamento.refresh()
    if event == sg.WINDOW_CLOSED:
        janela_parametros.close()
        break

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
        
    Carregamento['progressbar'].update(geracao+1)

    populacao = nova_populacao

Carregamento.close()

# Obtendo o melhor cromossomo após as gerações
melhor_cromossomo = max(populacao, key=fitness)
melhor_cromossomo = [1 if gene else 0 for gene in melhor_cromossomo]

# Cálculo do total de peso e valor dos livros selecionados geneticamente
valor_total = peso_total = 0
for c in range(len(melhor_cromossomo)):
    if melhor_cromossomo[c] == 1:
        valor_total += valores[c]
        peso_total += pesos[c]

# Definição de layout de tela de resultados
tela_resultados = [
    [sg.Text(f'Melhor Indivíduo: {melhor_cromossomo}')],
    [sg.Text(f'Valor Total: {valor_total}')],
    [sg.Text(f'Peso Total: {peso_total}')],
    [sg.Push(), sg.Button('Sair'), sg.Push(),sg.Button('Mostrar/Esconder Log')],
    [sg.Multiline(size=(60, 10), key='-LOG-',visible = False, autoscroll=True)]
]

# Exibindo resultados
janela_resultados = sg.Window('RESULTADOS', layout=tela_resultados)


log_visible = False

while True:
    e, v = janela_resultados.read(timeout=0.1)
    if e == sg.WINDOW_CLOSED or e == 'Sair':
        janela_resultados.close()
        break
    if e == 'Mostrar/Esconder Log':
        log_visible = not log_visible
        janela_resultados['-LOG-'].update(value='\n'.join(log), visible=log_visible)
        janela_resultados.refresh()
