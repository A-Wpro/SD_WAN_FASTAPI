# -*- coding: utf-8 -*-
"""networkx.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KASnFMcyoNS7dpO_igOnkAqXCctPCrQq
"""





import networkx as nx
import pulp
import random
import matplotlib.pyplot as plt
import cvxpy as cp
import numpy as np
import io
from PIL import Image

g = nx.to_directed(nx.barabasi_albert_graph(20, 2))
nx.draw(g, with_labels=True)
plt.savefig("test")
plt.show()
source = 0
target = 19

# dict des capacites
dict_d = {}
for i, j in g.edges:
    dict_d[i, j] = dict_d[j, i] = round(random.uniform(1.0, 20.0), 0)

print(dict_d)

nx.set_edge_attributes(g, dict_d, 'capacity')

# dict de la bande passante utilisée
dict_used = {}
for i, j in g.edges:
    dict_used[i, j] = dict_used[j, i] = min(round(random.uniform(1.0, 20.0), 0),dict_d[i, j])

print(dict_used)

# dict des ratio used/capa
dict_ratio = {}
for i, j in g.edges:
    dict_ratio[i, j] = dict_ratio[j, i] = dict_used[i,j]/dict_d[i,j]

print(dict_ratio)

# Triche
i= 9
j= 19
dict_used[i, j] = 10 
dict_d[i, j] = 11

# binary variable to state a link is chosen or not
var_dict = {}
for (i, j) in g.edges:
    x = pulp.LpVariable("x_(%s_%s)" % (i,j), cat=pulp.LpBinary)
    var_dict[i, j] = x

# instantiate pulp PB
prob = pulp.LpProblem("Shortest_Path_Problem", pulp.LpMinimize)

# objective function
prob += pulp.lpSum([var_dict[i, j] for i, j in g.edges]), "Total Nodes Count"

# constraintes
for node in g.nodes:
  # On commence par la source
    if node == source:
        prob += pulp.lpSum([var_dict[k, j] for k, j in g.edges if k == node]) == 1
  # On arrive à la destination
    elif node == target:
        prob += pulp.lpSum([var_dict[i, k] for i, k in g.edges if k == node]) == 1
  # Loi de la concervation
    else:
        prob += pulp.lpSum([var_dict[i, k] for i, k in g.edges if k == node]) - pulp.lpSum([var_dict[k, j] for k, j in g.edges if k == node]) == 0

# contraintes de capa
for (i, j) in g.edges:
    prob += var_dict[i, j] + dict_used[i, j] <= dict_d[i, j]

# solve
prob.solve()

print(pulp.LpStatus[prob.status])
print(pulp.value(prob.objective))

print("The shortest path is ")
for link in g.edges:
    if var_dict[link].value() == 1.0:
        print(link, end=" ")



"""# Essai avec CVXPY

objective = cp.Minimize()

"""



