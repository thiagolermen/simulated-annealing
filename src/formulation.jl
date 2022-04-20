using JuMP
using Formatting
using Dates
using Gurobi

let
# Check the imput argument 
if length(ARGS) != 1
    exit()
else
    filename = ARGS[1]
end

println(filename)
f = open(filename, "r")

# Read the number of vertices from the first line and save it in N
s = readline(f)         
NV = parse(Int, split(s," ")[1])
NE = parse(Int, split(s," ")[2])

# Initialize incidence matrix
I = zeros(Bool, NE, NV)
v1 = zeros(Int, NE)
v2 = zeros(Int, NE)

# Costs array
C = zeros(Int, NV)
# Values array
V = zeros(Int, NE)

# Read all the edges
i = 1
a = 1
while ! eof(f) 
    # Cost of vertices
    if i <= NV
        s = readline(f)         
        v, c = [parse(Int, num) for num in split(s, " ")]
        C[v] = c     
    # Edges and its costs
    else 
        s = readline(f)         
        u, v, c = [parse(Int, num) for num in split(s, " ")]
        # Include edge in the adj. matrix and add the cost
        I[a, u] = 1
        I[a, v] = 1
        V[a] = c
        v1[a] = u
        v2[a] = v
        a = a + 1
    end
    i = i + 1
end
close(f)



# Initialize the model and set a time limit
model = Model()
set_optimizer(model, Gurobi.Optimizer);
set_optimizer_attribute(model, "TimeLimit", 3600)
set_silent(model)

# Fomulation variables
@variable(model, X[1:NE], Bin);
@variable(model, Y[1:NV], Bin);

# Objective
@objective(model, Max, sum(V[a]*X[a] for a in 1:NE) - sum(C[v]*Y[v] for v in 1:NV))

# Constraints
# @constraint(model, R[a=1:NE, v=1:NV, w=1:NV], 2*X[a]*I[a,v]*I[a,w] <= I[a,v]*Y[v] + I[a,w]*Y[w])
@constraint(model, R[a=1:NE], 2*X[a] <= Y[v1[a]] + Y[v2[a]])

#@constraint(model, R[a=1:NE], sum(I[a, v] for v in 1:NV) == 2)

# Optimize the model
optimize!(model)

# Informations about the model and results
@show solution_summary(model)
end
