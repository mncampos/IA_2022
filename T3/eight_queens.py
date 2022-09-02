import random

def evaluate(individual):
    """
    Recebe um indivíduo (lista de inteiros) e retorna o número de ataques
    entre rainhas na configuração especificada pelo indivíduo.
    Por exemplo, no individuo [2,2,4,8,1,6,3,4], o número de ataques é 10.

    :param individual:list
    :return:int numero de ataques entre rainhas no individuo recebido
    """
    numAtaques = 0

    for rainha in range(8):
        for outrasRainhas in range(rainha+1, 8):
            diferenca = outrasRainhas - rainha
            #Testa se está na esquerda ou direita, ignoramos cima e baixo devido ao fato de não ser possível no problema esta ocorrencia
            if individual[rainha] == individual[outrasRainhas]:
                numAtaques += 1
            #Testa diagonais
            if individual[rainha] == individual[outrasRainhas] + diferenca:
                numAtaques += 1
            if individual[rainha] == individual[outrasRainhas] - diferenca:
                numAtaques += 1
    return numAtaques
        
def tournament(participants):
    """
    Recebe uma lista com vários indivíduos e retorna o melhor deles, com relação
    ao numero de conflitos
    :param participants:list - lista de individuos
    :return:list melhor individuo da lista recebida
    """
    numAtksMelhorParticipante = 999
    melhorParticipante = []

    for participante in participants:
        atks = evaluate(participante)
        if(atks < numAtksMelhorParticipante):
            melhorParticipante = participante
            numAtksMelhorParticipante = atks
    return melhorParticipante


def crossover(parent1, parent2, index):
    """
    Realiza o crossover de um ponto: recebe dois indivíduos e o ponto de
    cruzamento (indice) a partir do qual os genes serão trocados. Retorna os
    dois indivíduos com o material genético trocado.
    Por exemplo, a chamada: crossover([2,4,7,4,8,5,5,2], [3,2,7,5,2,4,1,1], 3)
    deve retornar [2,4,7,5,2,4,1,1], [3,2,7,4,8,5,5,2].
    A ordem dos dois indivíduos retornados não é importante
    (o retorno [3,2,7,4,8,5,5,2], [2,4,7,5,2,4,1,1] também está correto).
    :param parent1:list
    :param parent2:list
    :param index:int
    :return:list,list
    """
    individuo1 = []
    individuo2 = []
    #Copia
    for i in range(0, index):
        individuo1.append(parent1[i])
        individuo2.append(parent2[i])
    #Após o indice, faz o cruzamento
    for i in range(index, 8):
        individuo1.append(parent2[i])
        individuo2.append(parent1[i])
    return [individuo1, individuo2]


def mutate(individual, m):
    """
    Recebe um indivíduo e a probabilidade de mutação (m).
    Caso random() < m, sorteia uma posição aleatória do indivíduo e
    coloca nela um número aleatório entre 1 e 8 (inclusive).
    :param individual:list
    :param m:int - probabilidade de mutacao
    :return:list - individuo apos mutacao (ou intacto, caso a prob. de mutacao nao seja satisfeita)
    """
    probabilidade = random.uniform(0,1)
    if probabilidade < m:
        individual[random.randint(0, 7)] = random.randint(1, 8)
    return individual


def run_ga(g, n, k, m, e):
    """
    Executa o algoritmo genético e retorna o indivíduo com o menor número de ataques entre rainhas
    :param g:int - numero de gerações
    :param n:int - numero de individuos
    :param k:int - numero de participantes do torneio
    :param m:float - probabilidade de mutação (entre 0 e 1, inclusive)
    :param e:int - número de indivíduos no elitismo
    :return:list - melhor individuo encontrado
    """
    individuos = []
    numIndividuosGerados = 0

    #Gera individuos aleatorios
    while numIndividuosGerados < n:
        novo = []
        for i in range(0,8):
            novo.append(random.randint(1,8))
        individuos.append(novo)
        numIndividuosGerados += 1
    
    for geracao in range(g):
        nova_populacao = []
        if e == True:
            nova_populacao.append(tournament(individuos))
        
        while len(nova_populacao) < n:
            #Obtem x e y como random selection do algoritmo
            x = random.sample(individuos, k)
            y = random.sample(individuos, k)
            pai = tournament(x)
            mae = tournament(y)
            #Reproduz
            filhos = crossover(pai,mae, random.randint(1, 8))
            filho1 = mutate(filhos[0], m)
            filho2 = mutate(filhos[1],m)
            #Após mutação, adiciona a nova populaçao
            nova_populacao.append(filho1)
            nova_populacao.append(filho2)
        individuos = nova_populacao
    return tournament(individuos)



