# Simulated Annealing 

## About
This project aims to develop the simulated annealing metaheuristic to solve an Integer Programming problem. For sake of comparasion we are going to formulate the problem using JuMP achieving the results with Gurobi optimizer and also tun the instances using the metaheuristic defined above.

### Problem statement

Let $G = (V, E)$ a graph with costs $c_v \in \mathbb{Z}$ in each vertex $v \in V$ and values $v_a \in \mathbb{Z}$ in each edge $a \in E$. Find a subset of edges $A \subseteq E$ that maximized the sum of the values of the chosen edges less the costs of the vertices that were covered by those edges (a vertex is chosen by an edge when some incident edge to it is chosen by A).

### Instances and format
The instances are text files ```instance_n_m.dat``` where $n$ is the number of vertices and $m$ is the number of edges. The first line contains the integers $n$, $m$, separated by spaces. The next $n$ lines contain the integers $v$, $c$, separated by spaces, which corresponds to the cost $c$ of the vertex $v$. The last $m$ lines contain three integers $u$, $v$, $c$, separated by spaces, which corresponds to the edge $\{u, v\}$ with cost $c$. The vertices are indexed from 1 to $n$.

## Running the code

### Formulation
To run the Julia code, just execute the following command:

```console
cd src && julia formluation.jl <FILE>
```

Or you can just run the script file for all the instances executing the command:

```console
chmod +x script.sh && ./script.sh
```

The formulation results will be saved at ```src/formulation results```


### Metaheuristic
Tu run the metaheuristic using the Python script, execute the following command:

```console
python3 simulated_annealing.py -it <initial_temperature> \
 -ft <final_temperature> \
 -i <iterations> \
 -cr <cooling_rate> \
 -mi <metropolis_iterations> \
 -s <save_logfile_at>
```

This command will run all the instances included in the ```data``` directory.

## Results
Using the Gurobi optimizer and our own fomulation we could achieve optimal results for all instances.

Even though, using defined parameters set as default in the code, we could achieve results taht were close to the optimal.
