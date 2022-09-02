import math
import numpy as np

#data = np.genfromtxt('alegrete.csv', delimiter=',')

def compute_mse(theta_0, theta_1, data):
    """
    Calcula o erro quadratico medio
    :param theta_0: float - intercepto da reta
    :param theta_1: float -inclinacao da reta
    :param data: np.array - matriz com o conjunto de dados, x na coluna 0 e y na coluna 1
    :return: float - o erro quadratico medio
    """

    sum_part = []
    h0 = []

    #função de aproximação de pontos
    for x in data:
        h0.append(theta_0 + x[0] * theta_1)

    for colun, h0_atm in zip(data, h0):
        sum_part.append(math.pow((h0_atm * colun[0]) - colun[1], 2))
    
    sum_all = sum(sum_part)
    n = len(data)
    mse = 1/n * sum_all

    return mse

#compute_mse(1,1,data)


def step_gradient(theta_0, theta_1, data, alpha):
    """
    Executa uma atualização por descida do gradiente  e retorna os valores atualizados de theta_0 e theta_1.
    :param theta_0: float - intercepto da reta
    :param theta_1: float -inclinacao da reta
    :param data: np.array - matriz com o conjunto de dados, x na coluna 0 e y na coluna 1
    :param alpha: float - taxa de aprendizado (a.k.a. tamanho do passo)
    :return: float,float - os novos valores de theta_0 e theta_1, respectivamente
    """
    sum_parts = []
    expansion = []
    sum_derivative_theta1 = []
    n = len(data)

    for x in data:
        expansion.append(theta_0 + theta_1 * x[0])

    for colun, i in zip(data, expansion):
        sum_parts.append(i - colun[1])

    for x, i in zip(data, sum_parts):
        sum_derivative_theta1.append(i * x[0])

    #derivadas de theta0 e theta1
    derivative_theta0 = 2/n * sum(sum_parts) * 1
    derivative_theta1 = 2/n * sum(sum_derivative_theta1)

    new_theta0 = theta_0 - (alpha * derivative_theta0)
    new_theta1 = theta_1 - (alpha * derivative_theta1)
    
    return new_theta0, new_theta1
    
#step_gradient(1, 1, data, 0.1)
   

def fit(data, theta_0, theta_1, alpha, num_iterations):
    """
    Para cada época/iteração, executa uma atualização por descida de
    gradiente e registra os valores atualizados de theta_0 e theta_1.
    Ao final, retorna duas listas, uma com os theta_0 e outra com os theta_1
    obtidos ao longo da execução (o último valor das listas deve
    corresponder à última época/iteração).

    :param data: np.array - matriz com o conjunto de dados, x na coluna 0 e y na coluna 1
    :param theta_0: float - intercepto da reta
    :param theta_1: float -inclinacao da reta
    :param alpha: float - taxa de aprendizado (a.k.a. tamanho do passo)
    :param num_iterations: int - numero de épocas/iterações para executar a descida de gradiente
    :return: list,list - uma lista com os theta_0 e outra com os theta_1 obtidos ao longo da execução
    """

    sum_parts = []
    expansion = []
    sum_derivative_theta1 = []
    n = len(data)
    list_theta0 = []
    list_theta1 = []

    list_theta0.append(theta_0)
    list_theta1.append(theta_1)


    for i in range(num_iterations):
       
        for x in data:
            expansion.append(theta_0 + theta_1 * x[0])

        for colun, i in zip(data, expansion):
            sum_parts.append(i - colun[1])

        for x, i in zip(data, sum_parts):
            sum_derivative_theta1.append(i * x[0])

        #derivadas de theta0 e theta1
        derivative_theta0 = 2/n * sum(sum_parts) * 1
        derivative_theta1 = 2/n * sum(sum_derivative_theta1)

        new_theta0 = theta_0 - (alpha * derivative_theta0)
        new_theta1 = theta_1 - (alpha * derivative_theta1)

        list_theta0.append(new_theta0)
        list_theta1.append(new_theta1)

        theta_0 = new_theta0
        theta_1 = new_theta1

        sum_parts = []
        expansion = []
        sum_derivative_theta1 = []
        
    return list_theta0, list_theta1
