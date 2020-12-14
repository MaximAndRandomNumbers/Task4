import random

##Генетические операторы:
##Начальная популяция - жадный выбор
##Селекция - 20% лучших
##Скрещивание - по 3 точкам
##Мутация - добавление 1 случайной вещи
# (с данной мутацией результат не очень, я написал свою функцию, её вызов закомментирован,
# но с ней реузльтат лучше библиотечного (строка 196))
##Формирование новой популяции - штраф за старость
##Условие остановки определено экспериментально - 1000 поколений
##(изменения видны через 500 поколений, после 1000 поколений ничего не меняется)

data_file = "15.txt"

things = []
population = []

number_of_creatures = 200


def startGenetic():
    global population
    max_cost = 0
    cheapest_thing = min(things, key=lambda thing: thing['cost'])['cost']
    counter = 0
    generateStartPopulation()

    while (counter < 500):
        selected_creatures = select(population)
        new_creatures = crossingOver(selected_creatures)
        mutated_creatures = mutation(new_creatures)
        population = generateNewPopulation(population, mutated_creatures)
        counter += 1
        # Изменения происходят после нескольких поколений, так что проверять на каждой иттерации нет смысла
        # if result_found(max_cost, population, cheapest_thing):
        #     break
        max_cost = population[0]
    return population[0]


def result_found(prev_cost, population, eps):
    max_cost = population[0]['cost']
    print(max_cost)
    if abs(max_cost - prev_cost) <= eps:
        return True

    return False


def generateCreature():
    creature = {
        'code': [],
        'weight': 0,
        'volume': 0,
        'cost': 0,
        'fitness': 0
    }
    rand_thing = random.randint(0, len(things))
    creature['code'] = [0 for _ in range(len(things))]
    current_weight = 0
    current_volume = 0
    current_cost = 0
    for i in range(rand_thing, len(things)):
        if (current_volume + things[i]['volume'] > max_volume or
                current_weight + things[i]['weight'] > max_weight):
            break
        current_weight += things[i]['weight']
        current_volume += things[i]['volume']
        current_cost += things[i]['cost']
        creature['code'][i] = 1
    creature['weight'] = current_weight
    creature['volume'] = current_volume
    creature['cost'] = current_cost
    return creature


def generateStartPopulation():
    for i in range(number_of_creatures):
        population.append(generateCreature())
    return


def count_fitness_creature(creature):
    if creature['weight'] > max_weight or creature['volume'] > max_volume:
        creature['fitness'] = 0
    else:
        creature['fitness'] = creature['cost']
    return


def count_fitness(population):
    for creature in population:
        count_fitness_creature(creature)
    return


def select(population):
    count_fitness(population)
    selected_creatures = sorted(population, key=lambda creature: creature['fitness'], reverse=True)[
                         0:int(number_of_creatures * 0.2)]
    return selected_creatures


def create_creature_from_code(code):
    creature = {
        'code': code,
        'weight': 0,
        'volume': 0,
        'cost': 0,
        'fitness': 0
    }
    for i in range(0, len(creature['code'])):
        creature['weight'] += creature['code'][i] * things[i]['weight']
        creature['volume'] += creature['code'][i] * things[i]['volume']
        creature['cost'] += creature['code'][i] * things[i]['cost']

    if creature['weight'] > max_weight or creature['volume'] > max_volume:
        creature['fitness'] = 0
    else:
        creature['fitness'] = creature['cost']

    return creature


def cross_over(creature1, creature2):
    sequence = [i for i in range(0, len(creature1['code']))]
    rand_bits = []
    for i in range(3):
        rand_number = random.choice(sequence)
        rand_bits.append(rand_number)
        sequence.remove(rand_number)
    new_creature1_code = [bit for bit in creature1['code']]
    new_creature2_code = [bit for bit in creature2['code']]
    for bit in rand_bits:
        temp = new_creature1_code[bit]
        new_creature1_code[bit] = new_creature2_code[bit]
        new_creature1_code[bit] = temp

    return [create_creature_from_code(new_creature1_code), create_creature_from_code(new_creature2_code)]


def crossingOver(selected_creatures):
    new_creatures = []
    counter = 0
    while counter < len(selected_creatures) / 2:
        new_pair = cross_over(selected_creatures[counter], selected_creatures[len(selected_creatures) - counter-1])
        for creature in new_pair:
            new_creatures.append(creature)
        counter += 1
    return new_creatures


def mutate(creature):
    zeros = []
    for i in range(len(creature['code'])):
        if creature['code'][i] == 0:
            zeros.append(i)
    rand = random.choice(zeros)
    creature['code'][rand] = 1
    creature['weight'] += things[rand]['weight']
    creature['volume'] += things[rand]['volume']
    creature['cost'] += things[rand]['cost']

    count_fitness_creature(creature)
    return

def mutate_test(creature):
    zeros = []
    ones = []
    for i in range(len(creature['code'])):
        if creature['code'][i] == 0:
            zeros.append(i)
    for i in range(len(creature['code'])):
        if creature['code'][i] == 1:
            ones.append(i)
    rand1 = random.choice(zeros)
    rand2 = random.choice(ones)
    creature['code'][rand1] = 1
    creature['weight'] += things[rand1]['weight']
    creature['volume'] += things[rand1]['volume']
    creature['cost'] += things[rand1]['cost']
    creature['code'][rand2] = 0
    creature['weight'] -= things[rand2]['weight']
    creature['volume'] -= things[rand2]['volume']
    creature['cost'] -= things[rand2]['cost']
    count_fitness_creature(creature)
    return

def mutation(new_creatures):
    random.shuffle(new_creatures)

    for i in range(0, int(0.05 * len(new_creatures))):
        mutate(new_creatures[i])
        ##Даёт лучший результат, но по заданию использую  ту, что выше
        ##mutate_test(new_creatures[i])

    return new_creatures


def recount_fitness(population):
    for creature in population:
        creature['fitness'] *= 0.9


def generateNewPopulation(old_population, new_creatures):
    recount_fitness(old_population)
    old_population.extend(new_creatures)
    new_population = sorted(old_population, key=lambda creature: creature['fitness'], reverse=True)[
                     0:int(number_of_creatures)]
    return new_population


with open(data_file, 'r') as data:
    first_line = data.readline().split(" ")
    max_weight = int(first_line[0])
    max_volume = float(first_line[1])

    for line in data:
        line = line.rstrip("\n").split(" ")
        things.append({
            'weight': int(line[0]),
            'volume': float(line[1]),
            'cost': int(line[2])
        })

creature = startGenetic()
result_code = creature['code']
print(result_code)
print('Cost = ' + str(creature['cost']))
print('Weight = ' + str(creature['weight']))
print('Volume = ' + str(creature['volume']))

