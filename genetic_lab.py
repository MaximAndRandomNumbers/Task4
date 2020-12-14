from pyeasyga import pyeasyga

# setup data
data_file = "15.txt"
data = []
with open(data_file, 'r') as data_f:
    first_line = data_f.readline().split(" ")
    max_weight = int(first_line[0])
    max_volume = float(first_line[1])

    for line in data_f:
        line = line.rstrip("\n").split(" ")
        data.append((int(line[0]),float(line[1]),int(line[2])))


ga = pyeasyga.GeneticAlgorithm(data)        # initialise the GA with data
ga.population_size = 200                    # increase population size to 200 (default value is 50)

# define a fitness function
def fitness(individual, data):
    weight, volume, price = 0, 0, 0
    for (selected, item) in zip(individual, data):
        if selected:
            weight += item[0]
            volume += item[1]
            price += item[2]
    if weight > max_weight or volume > max_volume:
        price = 0
    return price

ga.fitness_function = fitness               # set the GA's fitness function
ga.run()                                    # run the GA
print(ga.best_individual())                 # print the GA's best solution