from queue import LifoQueue, PriorityQueue, Queue, SimpleQueue
import time
from dataclasses import dataclass, field

class Nodo:
    """
    Implemente a classe Nodo com os atributos descritos na funcao init
    """
    def __init__(self, estado, pai, acao, custo):
        """
        Inicializa o nodo com os atributos recebidos
        :param estado:str, representacao do estado do 8-puzzle
        :param pai:Nodo, referencia ao nodo pai, (None no caso do nó raiz)
        :param acao:str, acao a partir do pai que leva a este nodo (None no caso do nó raiz)
        :param custo:int, custo do caminho da raiz até este nó
        """
        # substitua a linha abaixo pelo seu codigo
        self.estado = estado
        self.pai = pai
        self.acao = acao
        self.custo = custo

# estado é uma string que contém 9 caracteres, onde o caracter _ simboliza a posição atual do jogo. Os 3 primeiros caracteres são referentes a primeira fileira do jogo, os próximos 3 se referem as do meio,
# e os ultimos 3 à ultima fileira.

#Definimos o 8-cube como 
# x0 x1 x2
# y3 y4 y5
# z6 z7 z8

def mapeiaCoordenadas(n):
    """
    Recebe um número que corresponde à posição atual do espaço vazio e retorna sua respectiva coordenada do cubo como uma string. Exemplo : mapeiaCoordenadas(1) -> 'x1' 
    :param n: int, representa a posição atual do espaço vazio
    """
    coordY = str(n)
    if n <= 2:
        return 'x' + coordY 
    elif n > 2 and n <= 5:
        return 'y' + coordY
    elif n > 5 and n <= 8:
        return 'z' + coordY

def move(estado, vazio, peça):
    """
    Realiza o swap entre o espaço vazio e a peça a ser movida. Retorna uma string como o estado novo.
    :param estado: lista, representa o estado como definido pelo professor. é necessário ser uma lista devido ao fato de strings não serem mutáveis em python, impossibilitando o swap.
    :param vazio: int, representa a posição que o espaço vazio se encontra
    :param peça: int, representa a posição da peça a ser deslizada
    """
    temp = estado[vazio]
    estado[vazio] = estado[peça]
    estado[peça] = temp
    str1 = ""
    return str1.join(estado)

def checaJogada(estado, jogada, posicao):
    """
    Recebe um estado e uma lista de possíveis jogadas e retorna uma tupla contendo as jogadas possiveis e o estado alterado
    :param estado: str, representa o estado como definido pelo professor.
    :param jogada: str, representa uma das jogadas possíveis
    :param posicao: int, representa a posição atual do espaço vazio
    """
    if jogada == "esquerda":
        return (jogada, move(estado, posicao, posicao-1 ) )
    elif jogada == "direita":
        return (jogada, move(estado, posicao, posicao+1))
    elif jogada == "acima" :
        return (jogada, move(estado, posicao, posicao-3 ))
    elif jogada == "abaixo" :
        return (jogada, move(estado, posicao, posicao+3))



def sucessor(estado):
    """
    Recebe um estado (string) e retorna uma lista de tuplas (ação,estado atingido)
    para cada ação possível no estado recebido.
    Tanto a ação quanto o estado atingido são strings também.
    :param estado:
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    jogadas = {
        "x0" : "direita, abaixo",
        "x1" : "esquerda, abaixo, direita",
        "x2" : "esquerda, abaixo",
        "y3" : "direita, abaixo, acima",
        "y4" : "esquerda, acima, abaixo, direita",
        "y5" : "esquerda, acima, abaixo",
        "z6" : "direita, acima",
        "z7" : "esquerda, acima, direita",
        "z8" : "esquerda, acima"
    }


    coords = mapeiaCoordenadas(estado.find('_'))  # retorna a coordenada da posiçao atual do jogo
    moves = jogadas[coords].split(", ") # armazena uma lista com as possíveis jogadas
    plays = []
    for jogada in moves:
        plays += [checaJogada(list(estado), jogada, (int(coords[1])))] 
    return plays

    




def expande(nodo):
    """
    Recebe um nodo (objeto da classe Nodo) e retorna um iterable de nodos.
    Cada nodo do iterable é contém um estado sucessor do nó recebido.
    :param nodo: objeto da classe Nodo
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    filhos = sucessor(nodo.estado)
    grafo = list()
    for filho in filhos:
        grafo.append(Nodo(filho[1], nodo, filho[0], nodo.custo+1))
    return grafo


def backtrack(nodo):
    """
    Dado um nodo, retorna o caminho até ele.
    """
    path = []
    path.append(nodo.acao)
    
    #inicia o backtrack
    nodo_atual = nodo.pai
    while (nodo_atual is not None):
        path.append(nodo_atual.acao)
        nodo_atual = nodo_atual.pai
    
    del path[-1] #retira o nodo raiz
    path.reverse()
    return path



def bfs(estado):
    """
    Recebe um estado (string), executa a busca em LARGURA e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    X = set()
    F = SimpleQueue()
    F.put(Nodo(estado, None, None, 0))

    if(estado == "12345678_"):
        return []

    while True:
        if F.empty():
            return None
        v = F.get()
       
        if v.estado == "12345678_":
            return backtrack(v)
        if v.estado not in X:
            X.add(v.estado)
            succesores = expande(v)
            for nodo in succesores:
                F.put(nodo)






def dfs(estado):
    """
    Recebe um estado (string), executa a busca em PROFUNDIDADE e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    X = set()
    F = LifoQueue()
    F.put(Nodo(estado, None, None, 0))

    if(estado == "12345678_"):
        return []

    while True:
        if F.empty():
            return None
        v = F.get()
       
        if v.estado == "12345678_":
            return backtrack(v)
        if v.estado not in X:
            X.add(v.estado)
            succesores = expande(v)
            for nodo in succesores:
                F.put(nodo)



@dataclass(order=True) #Classe com um Nodo e sua prioridade (para fins da implementação da fila de prioridades)
class prioridadeHeuristica:
    priority: int
    item: Nodo=field(compare=False)

class filaPrioridades(PriorityQueue): #fila de prioridades utilizando a funçao heuristica recebida
    def __init__(self, FuncaoHeuristica):
        super().__init__()
        self.FuncaoHeuristica = FuncaoHeuristica #calcula a distancia hamming dado um estado

    def put(self, caminho):
        super().put(prioridadeHeuristica(priority=self.FuncaoHeuristica(caminho.estado) + caminho.custo, item = caminho))
    
    def get(self):
        return super().get().item

def calculaHamming(estado):
    return sum(hamming1 != hamming2 for hamming1, hamming2 in zip ("12345678", estado))


def A_Estrela(estado, funcaoHeuristica):
    X = set()
    F = funcaoHeuristica()
    F.put(Nodo(estado, None, None,0))

    if(estado == "12345678_"):
        return []
    while True:
        if F.empty():
            return None
        v = F.get()

        if v.estado == "12345678_":
            return backtrack(v)
        if v.estado not in X:
            X.add(v.estado)
            sucessores = expande(v)
            for nodo in sucessores:
                F.put(nodo)

def astar_hamming(estado):
    """
    Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Hamming e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    return A_Estrela(estado, lambda: filaPrioridades(calculaHamming))


def distanciaManhattan(estado): #calcula a distancia manhattan dado estado

    puzzleCorreto = {
    "1":(0,0),
    "2":(0,1),
    "3":(0,2),
    "4":(1,0),
    "5":(1,1),
    "6":(1,2),
    "7":(2,0),
    "8":(2,1)
            }


    estimativaManhattan = 0
    pecas = ["1","2","3","4","5","6","7","8"]

    for peca in pecas:
        indice = estado.find(peca)
        coluna = indice % 3
        fileira = indice // 3
        estimativaManhattan += abs(puzzleCorreto[peca][0] - fileira) + abs(puzzleCorreto[peca][1] - coluna)
    
    return estimativaManhattan
    

def astar_manhattan(estado):
    """
    Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Manhattan e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    return A_Estrela(estado, lambda : filaPrioridades(distanciaManhattan))



##DEBUG ####################################################################################################################################################
"""
estado_teste = "123456_78"

tic = time.perf_counter()
resultado = bfs(estado_teste)
toc = time.perf_counter()
if resultado is not None:
    print(f"BFS com estado {estado_teste}: \n Tempo : {toc - tic:0.4f} segundos. \n Nós expandidos : {resultado[1]} \n Custo da solução : {len(resultado[0])}")  
else:
    print(f"BFS não encontrou solução. Tempo levado : {toc - tic:0.4f}")

tic = time.perf_counter()
resultado = dfs(estado_teste)
toc = time.perf_counter()
if resultado is not None:   
    print(f"DFS com estado {estado_teste}: \n Tempo : {toc - tic:0.4f} segundos. \n Nós expandidos : {resultado[1]} \n Custo da solução : {len(resultado[0])}")  
else:
    print(f"DFS não encontrou solução. Tempo levado : {toc - tic:0.4f}")

tic = time.perf_counter()
resultado = astar_hamming(estado_teste, lambda: filaPrioridades(calculaHamming))
toc = time.perf_counter()
if resultado is not None:
    print(f"A* Hamming com estado {estado_teste}: \n Tempo : {toc - tic:0.4f} segundos. \n Nós expandidos : {resultado[1]} \n Custo da solução : {len(resultado[0])}")  
else:
    print(f"A* Hamming não encontrou solução. Tempo levado : {toc - tic:0.4f}")

tic = time.perf_counter()
resultado = astar_manhattan(estado_teste, lambda: filaPrioridades(distanciaManhattan))
toc = time.perf_counter()
if resultado is not None:
    print(f"A* Manhattan com estado {estado_teste}: \n Tempo : {toc - tic:0.4f} segundos. \n Nós expandidos : {resultado[1]} \n Custo da solução : {len(resultado[0])}")  
else:
    print(f"A* Manhattan não encontrou solução. Tempo levado : {toc - tic:0.4f}")
"""