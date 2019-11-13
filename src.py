from auto_tuner import AutoTuner
import importlib.util

# initialise main path
main_path = '/Users/michal/PycharmProjects/MRP'

# name = 'ali535'
name = 'berlin11_modified'
# name = 'berlin52'
# name = 'fl417'
# name = 'gr666'
# name = 'kroA100'
# name = 'kroA150'
# name = 'nrw1379'
# name = 'pr2392'


# import Simulated Annealing project
spec_SA = importlib.util.spec_from_file_location('SimulatedAnnealing',
                                                 main_path + '/simulated_annealing/simulated_annealing.py')
SA = importlib.util.module_from_spec(spec_SA)
spec_SA.loader.exec_module(SA)

# import Tabu Search project
spec_TS = importlib.util.spec_from_file_location('TabooSearch', main_path + '/tabu_search/taboo_search.py')
TS = importlib.util.module_from_spec(spec_TS)
spec_TS.loader.exec_module(TS)

# import Genetic Algorithm project
spec_GA = importlib.util.spec_from_file_location('GeneticAlgorithm',
                                                 main_path + '/genetic_algorithm/genetic_algorithm.py')
GA = importlib.util.module_from_spec(spec_GA)
spec_GA.loader.exec_module(GA)



# initialise AutoTuner
tuner = AutoTuner(name, main_path + '/datasets/*.tsp')


# tune Simulated annealing
# best_param = tuner(SA.SimulatedAnnealing, 30, {'t_start': [10000, 11], 't_min': [10, 1]}, 'SA')

# tune Simulated annealing
# best_param = tuner(TS.TabooSearch, 3, {'taboo_list_size': [1, 30], 'count_of_neighbours': [1, 30],
#                                        'mutation_ratio': [0.01, 0.5], 'epochs': [1, 20]}, 'TS')


# tune Genetic Algorithm
best_param = tuner(GA.GeneticAlgorithm, 50, {'population_size': [5, 10], 'size_of_elite': [0, 5],
                                            'mutation_ratio': [0.01, 0.5], 'epochs': [1, 20]}, 'GA')

print(best_param)
tuner.plot_simply_stats()


