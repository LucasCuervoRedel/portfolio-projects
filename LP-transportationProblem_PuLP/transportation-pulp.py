from pulp import *
import pandas as pd
import numpy as np

# We begin by creating a list of the warehouse nodes (2 at first)
warehouses = ['A', 'B']

# Then we create a distionary of how many units each node can supply
supply = {'A': 1000, 'B': 4000}

# The we create a list of the customer nodes
customers = ['1', '2', '3', '4', '5']

# We also make a dictionary with the demand for each customer
demand = {
    '1': 500,
    '2': 900,
    '3': 1800,
    '4': 200,
    '5': 700
}

# Lastly, we create a list of the costs of transporting from each warehouse to each customer
costs = [
    [2, 4, 5, 2, 1], # warehouse A
    [3, 1, 3, 2, 3] # warehouse B
]

# Turning the cost list into a dictionary
costs_dict = makeDict([warehouses, customers], costs, 0)





# Now we are ready to define a 'prob' variable to contain the problem data
prob = LpProblem("Package Distribution Problem", LpMinimize)

# For calculating the costs, we need to generate arcs between all nodes and customers
Routes = [(w, c) for w in warehouses for c in customers]

# As with any LP problem, we must define the variables
# For this, we create a dictionary called 'vars'
vars = LpVariable.dicts("Route", (warehouses, customers), 0, None, LpInteger)

# The next step is to add the objective function to the prob variable
prob += (
    lpSum([vars[w][c] * costs_dict[w][c] for (w, c) in Routes]),
    "Sum_of_Transporting_Costs"
)

# The last step in any LP formulation is defininf the constraints
# The supply maximum constraints are added to prob for each supply node (warehouse)
for w in warehouses:
    prob += (
        lpSum([vars[w][c] for c in customers]) <= supply[w],
        f"Sum_of_Products_out_of_Warehouse_{w}",
    )

# The demand minimum constraints are added to prob for each demand node (customer)
for c in customers:
    prob += (
        lpSum([vars[w][c] for w in warehouses]) >= demand[c],
        f"Sum_of_Products_into_Bar{c}",
    )

# The last step is to write the problem data to an .lp file
prob.writeLP("TransportationProblem.lp")

# Now we can solve the problem
prob.solve()

# And print out the optimal values and objective function
print("Status:", LpStatus[prob.status])

for v in prob.variables():
    print(v.name, "=", v.varValue)

print("Total Cost of Ingredients per can = ", value(prob.objective))