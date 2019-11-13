from datasets import Datasets
from random import uniform
from tqdm import tqdm
from matplotlib import pyplot as plt
import numpy as np
from termcolor import colored


class AutoTuner:
    def __init__(self, set_name, path):
        self.data = Datasets(path)
        self.set_name = set_name
        self.tuning_stats = None
        self.tuning_name = None

    def __call__(self, algorithm, num_iterations, parameters, experiment_name):
        """
        This method searches for the best parameters for given algorithm using 'greedy' method
        :param algorithm: callable, method which constructs heuristic to be tuned
        :param num_iterations: number of iterations when optimisation performs
        :param parameters: dictionary in form of parameter {name: [minimal_value, maximum_value], ...}
        :return: results - an array with the best parameters found
        """
        print(colored('start parameters: ' + str(parameters), 'red'))
        algorithm_object = algorithm(self.data, self.set_name)

        results_distances = []
        results_params = []

        # optimise only one parameter
        epochs = tqdm(range(0, num_iterations))
        for _ in epochs:

            # set parameters
            temp_parameters = []
            for par in parameters.values():
                val = type(par[0])(uniform(par[0], par[1]))
                temp_parameters.append(val)

            # perform experiment
            result = algorithm_object(*temp_parameters, plot_figure=False)

            # update results lists
            results_distances.append(min(result.keys()))
            results_params.append(temp_parameters)

            # add additional text to progressbar
            description = 'current parameters: ' + ''.join(str(round(p, 2)) + ', ' for p in temp_parameters)
            description += 'best solution: {}'.format(round(min(result.keys()), 2))
            epochs.set_description(description)

        # update tuning statistics
        self.tuning_stats = [results_distances, results_params]
        self.tuning_name = experiment_name

        return results_params[np.argmin(results_distances)]

    def plot_simply_stats(self):

        params = self.tuning_stats[1][np.argmin(self.tuning_stats[0])]
        params = str([round(s, 2) for s in params])

        plt.scatter([*range(len(self.tuning_stats[0]))], self.tuning_stats[0], c='cornflowerblue')
        plt.scatter(np.argmin(self.tuning_stats[0]), min(self.tuning_stats[0]), c='limegreen')


        plt.ylim([0, int(max(self.tuning_stats[0]) * 1.2)])
        plt.ylabel('Best distance in epoch')
        plt.xlabel('Epoch of tuning')
        plt.title('Tuning for: ' + self.tuning_name + ', dataset: ' + self.set_name +
                  '\nBest params: ' + params)
        plt.show()
