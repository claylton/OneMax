# Imports necessários
import random
from deap import creator, base, tools, algorithms


# Definição dos valores e pesos de objetos possíveis
# valor, peso
objetos = [
    (4, 12),
    (2, 2),
    (2, 1),
    (1, 1),
    (10, 4)
]

# Peso máximo que a mochila permite
peso_maximo = 15

# Define o tipo fitness: Um objetivo com maximização
creator.create("FitnessMax", base.Fitness, weights=(1.0,))

# Define o tipo indivíduo: indivíduo do tipo list (array) com
# a fitness definida anteriormente.
creator.create("Individual", list, fitness=creator.FitnessMax)

# Toolbox para inicialização de componentes do algoritmo
toolbox = base.Toolbox()

# Atributo booleano criado de forma aleatório
toolbox.register("attr_bool",
    random.randint, 0, 1)

# Indivíduo (tipo Inidividual) criado a partir do atributo definido
# anteriormente. Ou seja, indivíduo do tipo booleano.
# São criados 100 indivíduos. initRepeat faz esse papel
toolbox.register("individual",
    tools.initRepeat, creator.Individual, toolbox.attr_bool, n=len(objetos))

# Criação da população, do tipo lista composto
# por indivíduos (individual)
toolbox.register("population",
    tools.initRepeat, list, toolbox.individual)

# Criação da função de fitness.
# A função recebe um indivíduo e retorna uma tupla
# que representa a avaliação do indivíduo
def evalKnap(individual):
    # O índividuo é definido por um array de 0 e 1
    # Em que 1 significa que o objeto correspondente a posição está inserido
    # E 0 que não está

    peso = 0
    valor = 0

    for i in range(len(individual)):
        if individual[i] == 1:
            v, p = objetos[i]
            peso += p
            valor += v

    # Se peso passar do limite, retornar fitness 0
    if peso > peso_maximo:
        return 0,
    # Se não passar fitness sendo a soma dos valores dos objetos
    else:
        return valor,

# registra a função de fitness
toolbox.register("evaluate", evalKnap)

# registro dos operadores
toolbox.register("mate", tools.cxTwoPoint) #crossover
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05) #mutação

# registro do método de seleção
toolbox.register("select", tools.selTournament, tournsize=3)

# tamanho da população
population = toolbox.population(n=300)


# iniciando o processo de evolução

NGEN=40 # número de gerações
for gen in range(NGEN):

    # O módulo algorithms implementa vários algoritmos evolucionários
    # Na documentação tem a lista:
    # https://deap.readthedocs.io/en/master/api/algo.html
    # varAnd aplica operações de mutação e crossover
    # cxpb: probabilidade de crossover
    # mutpb: probabilidade de mutação
    offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.1)

    # avalia cada indivíduo
    fits = toolbox.map(toolbox.evaluate, offspring)

    # associa cada indivíduo ao seu valor de fitness
    for fit, ind in zip(fits, offspring):
        ind.fitness.values = fit

    # aplica a seleção para gerar a nova população
    population = toolbox.select(offspring, k=len(population))

# retorna o k melhor indivíduos da última população
top10 = tools.selBest(population, k=10)

# Imprime o melhor
print(top10[0])

individual = top10[0]

peso = 0
valor = 0

for i in range(len(individual)):
    if individual[i] == 1:
        v, p = mochila[i]
        peso += p
        valor += v

print(peso, valor)