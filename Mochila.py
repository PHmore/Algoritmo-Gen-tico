
#! Documentar o que cada função faz de forma mais detalhada

#* Resolver bugs relacionados a números de base maior que 10 em pesos, valor, população, mochila.
#* Aparentemente o erro relacionado a pesos é como o número maior que 10 está se comportando na lista
#* O problema relacionado aos números maiores que 10 está inteiramente na definição do cromossomo e no uso de len para ler string
#*pois o número 11 é reconhecido como 2 1s gerando assim um cromossomo erroneo pois terá dois genes
#* Resolvido utilizando a conversão para lista inteira antes da definição da população inicial

#! Existe um erro no crossover que acontece quando o cromossomo possui somente um gene

#! Caso a mutação seja grande a casos de printar como resultado um cromossomo que não respeita a função fitness
#!ou seja possui peso maior que permitido
#! generalizando pois o erro pode não está somente na mutação o que aparentemente é verdade. 
#! Há casos onde o cromossomo escolhido ultrapassa o limite da mochila

#! Verificar como a taxa de mutação está se comportando e se está agindo corretamente

#* Resolver erro aparecendo ao fechar ou cancelar: resolvido utilizando exit()

#! Consertar identação no aparecimento do log

from PySimpleGUI import PySimpleGUI as sg
import random

sg.theme('Reddit')

def converter_int(string):  # Converte os elementos que foram lidos como string na interface em uma lista de inteiros

    """
    A função converte a lista de strings lida como entrada pela interface em uma lista de inteiros, para que os cálculos
    sejam realizados.
    :param string: lista de strings lida como entrada (string)
    :return: retorna a lista de strings convertida para lista de inteiros
    """

    lista_inteira = list()
    if ',' in string:
        string = string.replace(',', ' ')
    string = string.split(" ")

    for item in string:
        lista_inteira.append(int(item))

    #print(lista_inteira)
    return lista_inteira


def formatar_log(lista):

    """
    Formata a lista log, cuja função é registrar a população das gerações do algoritmo genético
    :param lista: a lista de população
    :return:
    """

    for i in lista:
        for j in range(0, len(i)):
            if i[j] is True:
                i[j] = 1
            elif i[j] is False:
                i[j] = 0


# Função onde recebe o cromossomo ler os genes e retorna o FITNESS
def fitness(cromossomo):

    """
    Faz o cálculo de aptidão do cromossomo passado como parâmetro, para que ao final os melhores cromossomos sejam
    selecionados para crossover.
    :param cromossomo: um elemento da população
    :return: 0, caso não seja um bom cromossomo; retorna a soma dos valores caso seja um bom cromossomo
    """

    soma_pesos = soma_valores = 0
    for d in range(len(cromossomo)):
        #print (d)
        #print (cromossomo)
        #print (pesos)
        if cromossomo[d] == 1:
            soma_pesos += pesos[d]
            soma_valores += valores[d]

    if soma_pesos > capacidade_mochila or soma_pesos < min(pesos):
        return 0
    else:
        return soma_valores


# Função de cruzamento genético
def crossover(pai1, pai2):

    """
    Faz a mistura de genes
    :param pai1: primeira lista de genes
    :param pai2: segunda lista de genes
    :return: retorna as duas listas com genes misturados
    """

    ponto_corte = random.randint(1, len(pai1)-1)
    filho1 = pai1[:ponto_corte] + pai2[ponto_corte:]
    filho2 = pai2[:ponto_corte] + pai1[ponto_corte:]
    return filho1, filho2


# Função de mutação
def mutacao(individuo):

    """
    Escolhe uma alelo aleatório para fazer mutação
    :param individuo: cromossomo a ser mutado
    :return: retorna o cromossomo com a mutação
    """

    posicao = random.randint(0, len(individuo)-1)
    individuo[posicao] = not individuo[posicao]
    return individuo


# Definição do layout da janela de inserção de dados
tela_parametros = [
    [sg.Text('Pesos dos livros:'), sg.Push(), sg.Input(key='pesos')],
    [sg.Text('Valores dos livros:'), sg.Push(), sg.Input(key='valores')],
    [sg.Text('Capacidade da mochila:'), sg.Input('', (5, 1), key='capacidade_mochila')],
    [sg.Text('Tamanho da população:'), sg.Input('', (5, 1), key='tamanho_populacao')],
    [sg.Text('Taxa de mutação [entre 0 e 1]:'), sg.Input('', (5, 1), key='taxa_mutacao')],
    [sg.Text('Número de gerações:'), sg.Input('', (5, 1), key='geracoes')],
    [sg.Push(), sg.Button('continuar',button_color=('white', 'DarkGreen')), sg.Push(), sg.Button('cancelar',button_color=('white', 'DarkRed')), sg.Push()]
]

def Error_pop (m_error):
    tela_erro = [
    [sg.Text(m_error)],
    [sg.Push(),sg.Button('OK', button_color=('white', 'DarkGreen')),sg.Push()]
]
    Error_view = sg.Window('Erro', tela_erro)
    while True:
        event, values = Error_view.read()
        if event == sg.WINDOW_CLOSED or event == 'OK':
            break

    Error_view.close()

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

        if not (v['tamanho_populacao'] and v['taxa_mutacao'] and v['valores'][:] and v['capacidade_mochila'] and v['pesos'][:] and v['geracoes']):
            Error_pop('ERROR: Preencha todos os campos')
            continue

        pesos = v['pesos'][:]
        valores = v['valores'][:]

        tamanho_populacao = int(v['tamanho_populacao'])
        taxa_mutacao = float(v['taxa_mutacao'])
        geracoes = int(v['geracoes'])
        capacidade_mochila = int(v['capacidade_mochila'])

        pesos = converter_int(pesos)
        valores = converter_int(valores)

        if (len(pesos) != len(valores) or len(pesos) <= 1 ):
            Error_pop('ERROR: A quantidade de pesos e valores devem ser a mesmas\nA quantidade deve ser maior que 1')
            continue            


        if (capacidade_mochila < min(pesos)):
            Error_pop('ERROR: Insira uma capacidade de mochila válida')
            continue

        if (geracoes <= 0 or tamanho_populacao <= 0):
            Error_pop('ERROR: Insira um valor valido em gerações/população')
            continue

        janela_parametros.close()
        break

# Barra de progresso
tela_aguarde = [
    [sg.Text('Progresso')],
    [sg.ProgressBar(geracoes, orientation='h', size=(20, 20), key='progressbar',bar_color=('DarkGreen','LightGrey'))]
]

Carregamento = sg.Window('Barra de Progresso', tela_aguarde)

# Janela de histórico
log_layout = [
    [sg.Multiline(size=(60, 10), key='-LOG-', autoscroll=True)]
]

janela_logs = sg.Window('LOG', layout=log_layout)
log = []

# Inicializando a população
#print(f'Printando pesos', pesos)
populacao = [[random.choice([0, 1]) for _ in range(len(pesos))] for _ in range(tamanho_populacao)]

# Algoritmo genético

for geracao in range(geracoes):
    formatar_log(populacao)
    log.append(f'- População da geração {geracao}:\n {populacao}\n')

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
    [sg.Push(),  sg.Push(), sg.Button('Mostrar/Esconder Log'),sg.Button('Sair',button_color=('white', 'DarkRed')), sg.Push()],
    [sg.Multiline(size=(60, 10), key='-LOG-', visible=False, autoscroll=True,background_color=('black'),text_color=('white'))]
]

# Exibindo resultados
janela_resultados = sg.Window('RESULTADOS', layout=tela_resultados)

log_visible = False

while True:
    e, v = janela_resultados.read(timeout=1)
    if e == sg.WINDOW_CLOSED or e == 'Sair':
        janela_resultados.close()
        break
    if e == 'Mostrar/Esconder Log':
        log_visible = not log_visible
        janela_resultados['-LOG-'].update(value='\n'.join(log), visible=log_visible)
        janela_resultados.refresh()
