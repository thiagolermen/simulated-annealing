# Simulated Annealing 

## About
This project aims to develop the simulated annealing metaheuristic to solve an Integer Programming problem. For sake of comparasion we are going to formulate the problem using JuMP achieving the results with its optimizer and also tun the instances using the metaheuristic defined above.

### Problem statement

Let $G = (V, E)$ a graph with costs $c_v \in \mathbb{Z}$ in each vertex $v \in V$ and values $v_a \in \mathbb{Z}$ in each edge $a \in E$. Find a subset of edges $A \subseteq E$ that maximized the sum of the values of the chosen edges less the costs of the vertices that were covered by those edges (a vertex is chosen by an edge when some incident edge to it is chosen by A).

## Running the code

### Formulation
To run the Julia code, just execute the following command:

```
cd src
julia formluation.jl <FILE>
```

Where:

    - <FILE>: problem instance path

Or you can just run the script file for all the instances executing the command:
```
chmod +x script.sh
./script.sh
```

The formulation results will be saved at ```src/formulation results```


### Metaheuristic
Tu run the metaheuristic using the Python script, execute the following command:

```
python3 simulated_annealing.py 
```

## Results