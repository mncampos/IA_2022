# Membros do grupo:
## Mateus Nunes Campos 
- Cartão 00268613 
- Turma B
## Milena Maciel
- Cartão 
- Turma A
## Felipe Rambo
- Cartão
- Turma A


# Estratégia de parada :
- O programa testa em cada iteração de MIN e MAX se é um estado de término, no nosso caso consideramos se a profundidade for maior que a escolhida pelo grupo (5), se não há mais
jogadas disponíveis, se não há movimentos legais, e se o tempo de execução superou 4.5 segundos.

# Função de avaliação :
## O grupo se baseou no artigo "An analysis of Heuristics in Othello" para a criação das heurísticas. 
- Diferença de peças : Esta heurística leva em consideração a diferença de peças entre os jogadores. No geral, minimizar as peças convertidas é uma boa estratégia. Consideramos um peso de 10 nesta heurística.
- Cantos : Os cantos do tabuleiro são os lugares mais valiosos, capturar eles pode trazer muita estabilidade para o jogo. Consideramos um peso de 200 nesta heurística, devido sua importância.
- Alcance aos cantos : Proximidade de um jogador aos cantos, peso de 40.
- Mobilidade : Diferença de jogadas legais entre os jogadores, peso de 15.
- Estabilidade : Esta heurística é complexa de calcular, então apenas fizemos uma tentativa considerando os discos na fronteira. Basicamente uma peça estável é uma que não pode ser convertida. Peso de 70.

- Os pesos foram testados, mas idealmente treinar uma IA para calibração seria uma boa prática. Há muita variação.

# Decisões de projeto :
- Foi implementado o algoritmo minimax com poda alfa-beta, utilizando uma profundidade máxima de 5, entretanto, devido as restrições de 5 segundos, o funcionamento do algoritmo
para se chegar em 4.5 segundos. Não foram realizadas melhorias extras.

# Dificuldades : 
- Dividir as tarefas deste trabalho entre o grupo se provou dificil, e entender como as heurísticas se comportam e calibrar os pesos também foi dificil. Houve necessidade de aprender Othello também, visto que ninguem do grupo havia jogado.

# Bibliografia :

- "An analysis of Heuristics in Othello" - https://courses.cs.washington.edu/courses/cse573/04au/Project/mini1/RUSSIA/Final_Paper.pdf
- Video sobre minimax alfa-beta - https://www.youtube.com/watch?v=l-hh51ncgDI
- Aulas do professor Anderson Tavares