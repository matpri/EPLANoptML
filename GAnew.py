# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 07:03:06 2015

@author: GGaregnani, MPrina

NB: pip install -U git+http://github.com/DEAP/deap
constrains not available in the stable version
"""

## 1.1 Types
from deap import base, creator
from termcolor import colored

## 1.2 Initialization
import random
from deap import tools


def GA(bounds, evaluate, weights, n_pop, n_gen, feasible=None, penalty=None):
    """ Excute the GA algorithms.

    :x:  range of variables to create a random grid
    :evaluate: function to evaluate
    :weights: negative minimization, positive maximization
    :n: size of population
    :ngen: number of generations
    :[feasible]: function for boundary constraints
    """

    min_b = list(zip(*bounds))[0]
    max_b = list(zip(*bounds))[1]

    creator.create("FitnessMin", base.Fitness, weights=weights)
    creator.create("Individual", list, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()

    list_attr = []
    for i, bnd in enumerate(bounds):
        attr = 'attr_l%i' % i
        toolbox.register(attr, random.randint, bnd[0], bnd[1])
        list_attr.append(toolbox.__getattribute__(attr))

    toolbox.__dict__.keys()
    toolbox.register("individual", tools.initCycle, creator.Individual,
                     list_attr, n=1)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("mate", tools.cxUniform,
                      indpb=0.5)
    toolbox.register("mutate", tools.mutUniformInt,
                     low=min_b, up=max_b, indpb=1.0/100)    
    toolbox.register("mutate_random", tools.mutUniformInt,
                     low=min_b, up=max_b, indpb=10.0/100)                 
#    toolbox.register("mutate", tools.mutPolynomialBounded,
#                     low=min_b, up=max_b, eta=1.0, indpb=1.0/100)
    toolbox.register("select", tools.selNSGA2)
    toolbox.register("evaluate", evaluate)

    if feasible:
        toolbox.decorate("evaluate", tools.DeltaPenality(feasible, penalty))

    pop = toolbox.population(n=n_pop)
#    pop0 = pop
    from Seed import seed_list
    for ind in seed_list:
        del pop[0]
        
        guess_ind = creator.Individual(ind)    
        pop.append(guess_ind)

#    print(pop0)
#    print(len(pop0), len(pop))
    pop0 = pop
    print (pop, len(pop))
    pop_back_up = pop[:]

    # Evaluate the entire population
#    fitnesses = list(map(toolbox.evaluate, pop))
    '''different from no_multi version'''
    fitnesses = map(toolbox.evaluate, pop)
    # fitnesses = toolbox.map(toolbox.evaluate, pop)
    ff0 = fitnesses
#    print (colored(ff0, 'red'))
    
    for ind, fit in list(zip(pop, fitnesses)):
        ind.fitness.values = fit
        
    for ind, fit in list(zip(pop_back_up, fitnesses)):
        ind.fitness.values = fit 
    
    ff0 = [ind.fitness.values for ind in pop]
    hist = {'population': {}, 'fitness': {}}
    hist['population'][0] = list(pop0) #list(zip(*pop0))
    hist['fitness'][0] = list(ff0) #list(zip(*ff0))

    pop = toolbox.select(pop, len(pop))

    for gen in range(1, n_gen):
        print('step: ', colored(gen, 'red'))

        offspring = tools.selTournamentDCD(pop, len(pop))
        offspring = [toolbox.clone(ind) for ind in offspring]

        threshold = 0.85*(gen/n_gen)**0.5
        print(threshold)
        
        if random.random() < threshold:
            for ind1, ind2 in list(zip(offspring[::2], offspring[1::2])):
                if random.random() <= 0.9:
                    toolbox.mate(ind1, ind2)
    
                toolbox.mutate(ind1)
                toolbox.mutate(ind2)
                del ind1.fitness.values, ind2.fitness.values
        else:
            for ind1, ind2 in list(zip(offspring[::2], offspring[1::2])):
                if random.random() <= 0.9:
                    toolbox.mate(ind1, ind2)
    
                toolbox.mutate_random(ind1)
                toolbox.mutate_random(ind2)
                del ind1.fitness.values, ind2.fitness.values            

        invalids = [indiv for indiv in offspring if not indiv.fitness.valid]
#        print('invalids', invalids)
        
        for ind in offspring:
            if ind in invalids:    
                if ind in pop_back_up:
#                    print('YESSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS', ind)
                    for ind2 in pop_back_up:
                        if ind2==ind:
#                            print('found', ind2.fitness.values )
                            ind.fitness.values = ind2.fitness.values

        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        
        for ind, fit in list(zip(invalid_ind, fitnesses)):
            ind.fitness.values = fit

        for ind in invalid_ind:
            pop_back_up.append(ind)

        pop = toolbox.select(pop + offspring, n_pop)
#        print (pop)
#        pop_hist.append(pop)
        fitnesses = [ind.fitness.values for ind in pop]
        hist['population'][gen] = list(pop) #list(zip(*pop))
#        fitnesses = [ind.fitness.values for ind in pop]
        hist['fitness'][gen] = list(fitnesses)#list(zip(*fitnesses))

    ff=fitnesses
    
#    history={'populations': pop_hist, 'fitness': fit_hist}

    return pop, ff, hist#(pop0, pop), (ff0, ff), hist
