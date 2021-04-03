# -*- coding: utf-8 -*-
"""Min_bandwidth_Problem.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/10Mh83FUPdBGc3_bzYXoYDOfLxGkLM_Bg
"""


import networkx as nx
import pulp
import random
import matplotlib.pyplot as plt

g = nx.to_directed(nx.barabasi_albert_graph(20, 2))
nx.draw(g, with_labels=True)
plt.show()

source = 0
target = 17

dict_capa = {}
for i, j in g.edges:
    dict_capa[i, j] = dict_capa[j, i] = round(random.uniform(1.0, 20.0), 0)

nx.set_edge_attributes(g, dict_capa, 'capacity')

dict_used = {}
for i, j in g.edges:
    dict_used[i, j] = dict_used[j, i] = min(round(random.uniform(1.0, 20.0), 0),dict_capa[i, j])

nx.set_edge_attributes(g, dict_used, 'used')

dict_ratio = {}
for i, j in g.edges:
    dict_ratio[i, j] = dict_ratio[j, i] = dict_used[i, j]/dict_capa[i, j]

nx.set_edge_attributes(g, dict_ratio, 'ratio')

# instantiate
prob = pulp.LpProblem("Min_bandwidth_Problem", pulp.LpMinimize)
cost = nx.get_edge_attributes(g, 'ratio')

# binary variable to state a link is chosen or not
var_dict = {}
for (i, j) in g.edges:
    x = pulp.LpVariable("x_(%s_%s)" % (i,j), cat=pulp.LpBinary)
    var_dict[i, j] = x

# objective function
prob += pulp.lpSum([cost[i, j] * var_dict[i, j] for i, j in g.edges]), "Total bandwidth ratio Count"

# constraints
for node in g.nodes:
    rhs = 0
    if node == source:
        rhs = -1
    elif node == target:
        rhs = 1
    prob += pulp.lpSum([var_dict[i, k] for i, k in g.edges if k == node]) - \
            pulp.lpSum([var_dict[k, j] for k, j in g.edges if k == node]) == rhs

# constraints on capacity
packet_size = 1
for i,k in g.edges:
  prob += var_dict[i, k]*packet_size + dict_used[i,k]  <= dict_capa[i,k]

# solve
prob.solve()

print(pulp.LpStatus[prob.status])
print(pulp.value(prob.objective))
print("The shortest path is ")
for link in g.edges:
    if var_dict[link].value() == 1.0:
        print(link, end=" , ")

path = [(0, 13) , (13, 17)] 
for key,values in dict_ratio.items():
  if (key in path):
    print(key)
    print(values)