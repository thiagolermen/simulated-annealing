import os
import glob
import math
import time
import random
import argparse
import logging
import matplotlib.pyplot as plt
import pathlib as pl
from datetime import datetime


def parse_args():
    parser = argparse.ArgumentParser(description="Simulated annealing parameters")
    parser.add_argument('--initial_temperature', "-it", type=float, default=0.99)
    parser.add_argument('--final_temperature', "-ft", type=float, default=0.2)
    parser.add_argument('--iterations', "-i", type=int, default=100)
    parser.add_argument('--cooling_rate', "-cr", type=float, default=0.99)
    parser.add_argument('--metropolis_iterations', "-mi", type=int, default=1000)
    parser.add_argument('--save_at', "-s", type=str, default='/home/tslermen/Documents/simulated-annealing/src/metaheuristic_results')
    return parser.parse_args()


def parse_pair_int(s):
    a, b = s.split(" ")
    a = int(a)
    b = int(b)
    return a, b


def parse_triple_int(s):
    a, b, c = s.split(" ")
    a = int(a)
    b = int(b)
    c = int(c)
    return a, b, c


def read_file(filename):
    filepath = os.path.join("../data/", filename)
    
    with open(filepath, "r") as f:
        total_vertices, total_edges = parse_pair_int(f.readline())
        vertices_costs = [0 for i in range(total_vertices)]
        edges_costs = [0 for i in range(total_edges)]
        graph = [[0 for j in range(2)] for i in range(total_edges)]

        for _ in range(total_vertices):
            v, c = parse_pair_int(f.readline())
            vertices_costs[v-1] = c

        for i in range(total_edges):
            u, v, c = parse_triple_int(f.readline())
            edges_costs[i] = c
            graph[i][0] = u-1
            graph[i][1] = v-1
    
    return total_vertices, total_edges, vertices_costs, edges_costs, graph


def get_files():
    dataset_files = []
    for f in glob.glob("/home/tslermen/Documents/simulated-annealing/data/instance*.dat"):
        dataset_files.append(os.path.basename(f))

    return dataset_files


class Simulated_Annealing():
    def __init__(self, filename, initial_solution, initial_temperature, iterations, metropolis_iterations, cooling_rate):
        self.filename = filename
        self.total_vertices, \
        self.total_edges, \
        self.vertices_costs, \
        self.edges_costs, \
        self.graph = read_file(self.filename)
        self.initial_solution = initial_solution
        self.initial_temperature = initial_temperature
        self.final_temperature = final_temperature
        self.iterations = iterations
        self.metropolis_iterations = metropolis_iterations
        self.cooling_rate = cooling_rate
        self.all_objective_values = []
        self.total_iterations = 0

    def run(self):
        """Run the simulated annealing heuristic using the parameters given as input

        Return: List[List] the best found solution, Int the best objective value calculated
        """
        temperature = self.initial_temperature
        best_solution = self.initial_solution
        solution = self.initial_solution
        objective_value = 0
        objective_best_value = 0

        while temperature >= self.final_temperature:
            for _ in range(self.iterations):
                solution, objective_value = self.metropolis(solution, temperature, objective_value)
                # For sake of comparasion  
                self.all_objective_values.append(objective_best_value)
                self.total_iterations += 1
                if objective_value > objective_best_value:
                    objective_best_value = objective_value
                    best_solution = solution

            temperature = self.cooling_rate*temperature
                
        return best_solution, objective_best_value

    def metropolis(self, solution, temperature, objective_value):
        """Run the metropilis algorithm using the given parameters

        Args:
            - solution: current solution
            - temperature: current temperature
            - objective_value: current objective value based on the current temperature

        Return: List[List] best found solution found using the algorithm, Int best objective value found
        """
        for _ in range(self.iterations):
            neighbor, neighbor_objective_value = self.choose_neighbor(solution, objective_value)
            delta = neighbor_objective_value - objective_value

            if delta >= 0:
                solution = neighbor
                objective_value = neighbor_objective_value
            else:
                threshold = random.random() 
                probability = self.boltzmann(delta, temperature)
                if threshold < probability:
                    solution = neighbor
                    objective_value = neighbor_objective_value


        return solution, objective_value
    
    def choose_neighbor(self, solution, objective_value):
        """Choose a random naighbor based on the current solution
        Args:
            - solution: current solution
            - objective_value: current objetive value
        """
        index = random.randint(0, len(self.graph)-1)
        edge = self.graph[index]
        neighbor = solution[:]
        if edge in neighbor:
            neighbor.remove(edge)
            objective_value = self.objective(neighbor, objective_value, edge, index, remove=True)      
        else:         
            objective_value = self.objective(neighbor, objective_value, edge, index, remove=False)
            neighbor.append(edge)

        return neighbor, objective_value

    def objective(self, solution, objective_value, edge, edge_index, remove):
        """Calculates the updated objective value based on the new neighbor structure
        Args:
            - solution: current solution
            - objective)value: current objective value
            - edge: edge that is going to be either removed or added
            - edge_index: index of the edge that is going to be either removed or added
            - remove: boolean taht defines if the edge is going to be either removed or added
        """
        if remove:
            objective_value -= self.evaluate_edge(solution, edge, edge_index)
        else:
            objective_value += self.evaluate_edge(solution, edge, edge_index)

        return objective_value

    def evaluate_edge(self, solution, edge, edge_index):
        """Evaluated the edge based on the current solution. If the edge is already in the solution
        it is not necessary to subtract its cost from the solution

        Args:
            - solution: current solution
            - edge: edge that is going to be either removed or added
            - edge_index: index of the edge that is going to be either removed or added
        """
        value = self.edges_costs[edge_index]
        setson = set([i[0] for i in solution]+[i[1] for i in solution])
        if edge[0] not in setson:
            value -= self.vertices_costs[edge[0]]
        if edge[1] not in setson:
            value -= self.vertices_costs[edge[1]]

        return value

    def boltzmann(self, x, temperature):
        e = math.e
        exponent = x / temperature
        return e ** exponent

    def plot_solutions(self, save_at):
        plt.plot(range(self.total_iterations),  self.all_objective_values)
        plt.ylabel('Objective value')
        plt.xlabel('Iterations')
        plt.title(os.path.basename(self.filename)[:-4])
        plt.savefig(f'{save_at}/{os.path.basename(self.filename)[:-4]}.jpg')
        plt.close()

if __name__ == '__main__':

    args = parse_args()
    dataset_files = get_files()

    # Parameters
    initial_solution = []
    initial_temperature = args.initial_temperature
    final_temperature = args.final_temperature
    iterations = args.iterations
    metropolis_iterations = args.metropolis_iterations
    cooling_rate = args.cooling_rate
    now = datetime.now()
    datetime = now.strftime("%d-%m-%Y-%H:%M:%S")
    save_at = f'{args.save_at}/it{initial_temperature}-if{final_temperature}-i{iterations}-mi{metropolis_iterations}-r{cooling_rate}'

    pl.Path(save_at).mkdir(parents=True, exist_ok=True)
    logging.basicConfig(filename=f'{save_at}/log-{datetime}.txt',
                        filemode='a',
                        level=logging.INFO)

    logging.info(f'Simulated annealing parameters: initial_temperature: {initial_temperature}, \
        final_temperature: {final_temperature}, iterations: {iterations}, metropolis_iterations: {metropolis_iterations}, \
        cooling_rate: {cooling_rate}')
    for instance in dataset_files:
        
        
        logging.info(f'Running simulated annealing with {instance}')

        initial_time = time.time()
        simulated_annealing = Simulated_Annealing(f"/home/tslermen/Documents/simulated-annealing/data/{instance}", 
                                                    initial_solution, 
                                                    initial_temperature, 
                                                    iterations, metropolis_iterations, 
                                                    cooling_rate
                                                )

        solution, objective_value = simulated_annealing.run()

        final_time = time.time()
        total_time = final_time - initial_time
        logging.info(f'Total running time: {total_time}s')

        simulated_annealing.plot_solutions(save_at)

        logging.info(f'Best solution: \n{solution}')
        logging.info(f'Best objective value: {objective_value}\n')
