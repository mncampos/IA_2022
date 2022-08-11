import math
import time

#Constantes
MIN = float('-inf')
MAX = float('inf')
MAX_DEPTH = 5


def make_move(the_board, color):
    start = time.perf_counter() #Inicia o temporizador
    jogada = maxValue(the_board, color , start, alpha = MIN, beta = MAX, depth = 0)
    return jogada[1]

def maxValue(board, color, start_time, alpha, beta, depth):
    if (time.perf_counter() - start_time > 4.5): #Se o tempo está para chegar no limite, para de avaliar
        return (avaliaJogada(board,color), (-1,-1))
    if board.is_terminal_state() or depth > MAX_DEPTH:      #Se não há jogadas disponíveis ou a profundidade estiver maior que o limite setado pelo grupo
        return (avaliaJogada(board,color), (-1,-1))
    if board.has_legal_move(color) == False and depth == 0: #Se não há jogadas legais 
        return (avaliaJogada(board,color), (-1,-1))

    legal_plays = board.legal_moves(color)
    jogada = (MIN, (-1,-1)) #Uma jogada é composta de (v, play), onde v é o valor da jogada e play a jogada em si

    if len(legal_plays) != 0:
        for play in legal_plays:
            boardCopy = board.copy()   #Copia o board e testa a jogada 
            boardCopy.process_move(play, color)
            resultado = minValue(boardCopy, board.opponent(color), start_time, alpha, beta, depth+1) #chama min e testa os valores
            if resultado[0] > jogada[0]:
                jogada = (resultado[0], play)
            else: jogada = (jogada[0], jogada[1])

            alpha = max(alpha, jogada[0])
            if alpha >= beta:  #poda
                break
        return jogada
    else:                               #se não há movimentos válidos, processa o movimento nulo
            boardCopy = board.copy()
            boardCopy.process_move((-1,-1), color)
            resultado = minValue(boardCopy, board.opponent(color), start_time, alpha, beta, depth+1)
            if resultado[0] > jogada[0]:
                jogada = (resultado[0], (-1,-1))
            else: jogada = (jogada[0], jogada[1])

            alpha = max(alpha, jogada[0])
            if alpha >= beta:
                return jogada
            return jogada
        



def minValue(board, color, start_time, alpha, beta, depth):
    if (time.perf_counter() - start_time > 4.5):
        return (avaliaJogada(board,color), (-1,-1))
    if board.is_terminal_state() or depth > MAX_DEPTH:      #Se não há jogadas disponíveis ou a profundidade estiver maior que o limite setado pelo grupo
        return (avaliaJogada(board,color), (-1,-1))
    if board.has_legal_move(color) == False and depth == 0: #Se não há jogadas legais e é o inicio do jogo
        return (avaliaJogada(board,color), (-1,-1))

    legal_plays = board.legal_moves(color)
    jogada = (MAX, (-1,-1))

    if len(legal_plays) != 0:
        for play in legal_plays:
            boardCopy = board.copy()
            boardCopy.process_move(play, color)
            resultado = maxValue(boardCopy, board.opponent(color), start_time, alpha, beta, depth+1)
            if resultado[0] < jogada[0]:
                jogada = (resultado[0], play)
            else: jogada = (jogada[0], jogada[1])

            beta = min(beta, jogada[0])
            if beta <= alpha:
                break
        return jogada
    else:
            boardCopy = board.copy()
            boardCopy.process_move((-1,-1), color)
            resultado = maxValue(boardCopy, board.opponent(color), start_time, alpha, beta, depth+1)
            if resultado[0] < jogada[0]:
                jogada = (resultado[0], (-1,-1))
            else: jogada = (jogada[0], jogada[1])

            beta = min(beta, jogada[0])
            if beta <= alpha:
                return jogada
            return jogada



#Heurísticas baseadas no artigo https://courses.cs.washington.edu/courses/cse573/04au/Project/mini1/RUSSIA/Final_Paper.pdf

def avaliaJogada(board, color):
    board_copy = board.copy()
    opponent_color = board.opponent(color)


    maxPieces = board.num_pieces(color)
    maxFrontierPieces = 0
    minPieces = board.num_pieces(opponent_color)
    minFrontierPieces = 0

    #Heuristicas utilizadas

    #Heurística que leva em conta a diferença entre peças dos jogadores
    pieceDifferenceHeuristic = 0

    #Tentativa de calcular a estabilidade das peças, se baseando nos discos de fronteira
    stabilityHeuristic = 0

    #Heuristica de controle dos canteiros
    cornerHeuristic = 0

    #Heuristica de aproximação dos canteiros
    cornerReachHeuristic = 0

    #Heuristica de mobilidade
    mobilityHeuristic = 0


    #Para visitar vizinhos
    X_row = [-1, -1, 0, 1, 1, 1, 0, -1]
    Y_column = [0, 1, 1, 1, 0, -1, -1, -1]

    for i in range(8):
        for j in range(8):
            if board.tiles[i][j] != '.':
                for z in range(8):
                    x = i + X_row[z]
                    y = j + Y_column[z]
                    if ( x >= 0 and x < 8 and y >= 0 and y < 8 and board.tiles[x][y] == '.'):
                        if board.tiles[i][j] == color:
                            maxFrontierPieces += 1
                        else: minFrontierPieces += 1
                        break
    
    if maxPieces > minPieces:
        pieceDifferenceHeuristic = (100 * maxPieces) / (maxPieces + minPieces)
    elif maxPieces < minPieces:
        pieceDifferenceHeuristic = -(100 * maxPieces) / (maxPieces + minPieces)
    elif maxPieces == minPieces:
        pieceDifferenceHeuristic = 0

    if maxFrontierPieces > minFrontierPieces:
        stabilityHeuristic = -(100 * maxFrontierPieces) / (maxFrontierPieces + minFrontierPieces)
    elif maxFrontierPieces < minFrontierPieces:
        stabilityHeuristic = (100 * minFrontierPieces) / (maxFrontierPieces + minFrontierPieces)
    elif maxFrontierPieces == minFrontierPieces:
        stabilityHeuristic = 0
    
    MAX_corners = 0
    MIN_corners = 0
    MAX_cornerReach = 0
    MIN_cornerReach = 0

    corner_coords = [0, 7 , 56, 63]
    board_copy_str = board_copy.__str__()

    for coord in corner_coords:
        if board_copy_str[coord] == color: #Se for de MAX, adiciona um ponto
            MAX_corners += 1
        elif board_copy_str[coord] == opponent_color:
            MIN_corners += 1
        elif board_copy_str[coord] == '.':    #Se for vazio, atribue um score Reach para quem tiver no alcance do canto
            match coord:
                case 0:
                    if board_copy.tiles[0][1] == color:
                        MAX_cornerReach += 1
                    elif board_copy.tiles[0][1] == opponent_color:
                        MIN_cornerReach += 1
                    if board_copy.tiles[1][1] == color:
                        MAX_cornerReach += 1
                    elif board_copy.tiles[1][1] == opponent_color:
                        MIN_cornerReach += 1
                    if board_copy.tiles[1][0] == color:
                        MAX_cornerReach += 1
                    elif board_copy.tiles[1][0] == opponent_color:
                        MIN_cornerReach += 1
                        
                case 7:
                    if board_copy.tiles[0][6] == color:
                        MAX_cornerReach += 1
                    elif board_copy.tiles[0][6] == opponent_color:
                        MIN_cornerReach += 1
                    if board_copy.tiles[1][6] == color:
                        MAX_cornerReach += 1
                    elif board_copy.tiles[1][6] == opponent_color:
                        MIN_cornerReach += 1
                    if board_copy.tiles[1][7] == color:
                        MAX_cornerReach += 1
                    elif board_copy.tiles[1][7] == opponent_color:
                        MIN_cornerReach += 1
                case 56:
                    if board_copy.tiles[7][1] == color:
                        MAX_cornerReach += 1
                    elif board_copy.tiles[7][1] == opponent_color:
                        MIN_cornerReach += 1
                    if board_copy.tiles[6][1] == color:
                        MAX_cornerReach += 1
                    elif board_copy.tiles[6][1] == opponent_color:
                        MIN_cornerReach += 1
                    if board_copy.tiles[6][0] == color:
                        MAX_cornerReach += 1
                    elif board_copy.tiles[6][0] == opponent_color:
                        MIN_cornerReach += 1
                case 63:
                    if board_copy.tiles[6][7] == color:
                        MAX_cornerReach += 1
                    elif board_copy.tiles[6][7] == opponent_color:
                        MIN_cornerReach += 1
                    if board_copy.tiles[6][6] == color:
                        MAX_cornerReach += 1
                    elif board_copy.tiles[6][6] == opponent_color:
                        MIN_cornerReach += 1
                    if board_copy.tiles[7][6] == color:
                        MAX_cornerReach += 1
                    elif board_copy.tiles[7][6] == opponent_color:
                        MIN_cornerReach += 1

    
    cornerHeuristic = 25 * (MAX_corners - MIN_corners)
    cornerReachHeuristic = -12.5 * (MAX_corners - MIN_corners)

    MAX_moves = len(board_copy.legal_moves(color))
    MIN_moves = len(board_copy.legal_moves(opponent_color))
    
    if MAX_moves > MIN_moves:
        mobilityHeuristic = (100 * MAX_moves) / (MAX_moves + MIN_moves)
    elif MAX_moves < MIN_moves:
        mobilityHeuristic = -(100 * MIN_moves) / (MAX_moves + MIN_moves)
    elif MAX_moves == MIN_moves:
        mobilityHeuristic = 0




    return (10 * pieceDifferenceHeuristic) + (200 * cornerHeuristic) + (40 * cornerReachHeuristic) + (15 * mobilityHeuristic) + (70 * stabilityHeuristic)