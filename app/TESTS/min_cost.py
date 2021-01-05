# -*- coding: utf-8 -*-
"""Min_cost.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xItULYLPPoO_Kc8JY4msTpeIMhkkVLbr
"""


import networkx as nx
import pulp
import random
import matplotlib.pyplot as plt

def min_cost(src, trg):
        
    g = nx.to_directed(nx.barabasi_albert_graph(20, 2)) #creation du network
    nx.draw(g, with_labels=True) #dessiner le graph
    plt.show()
    
    source = src #par ou il commence
    target = trg #vers ou il se dirige pour terminer
    
    dict_capa = {} # capacité de chaque node (debut , fin) entre 1 et 20
    for i, j in g.edges:
        dict_capa[i, j] = dict_capa[j, i] = round(random.uniform(1.0, 20.0), 0)
    
    nx.set_edge_attributes(g, dict_capa, 'capacity')
    
    dict_used = {} #capacite deja utilisé du noeud
    for i, j in g.edges:
        #meme valeur a l'allee et au retour
        dict_used[i, j] = dict_used[j, i] = min(round(random.uniform(1.0, 20.0), 0),dict_capa[i, j])
    
    nx.set_edge_attributes(g, dict_used, 'used')
    
    dict_cost = {} # le delay de passage d'un noeuf a un autre
    for i, j in g.edges:
        dict_cost[i, j] = dict_cost[j, i] = round(random.uniform(1.0, 20.0), 2)
    
    nx.set_edge_attributes(g, dict_cost, 'delay')
    
    path = [(3, 12) , (7, 3) , (12, 2) , (14, 7)] 
    for key,values in dict_cost.items():
      if (key in path):
        print(key)
        print(values)
    
    # instantiate
    prob = pulp.LpProblem("Min_Cost_Problem", pulp.LpMinimize)
    cost = nx.get_edge_attributes(g, 'delay')
    
    # binary variable to state a link is chosen or not
    var_dict = {}
    for (i, j) in g.edges:
        x = pulp.LpVariable("x_(%s_%s)" % (i,j), cat=pulp.LpBinary)
        var_dict[i, j] = x
    
    # objective function
    prob += pulp.lpSum([cost[i, j] * var_dict[i, j] for i, j in g.edges]), "Total Hop Count"
    
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
    
    out = []
    
    print(pulp.LpStatus[prob.status])
    out.append(pulp.LpStatus[prob.status])
    print(pulp.value(prob.objective))
    out.append(pulp.value(prob.objective))
    
    print("The shortest path is ")
    for link in g.edges:
        if var_dict[link].value() == 1.0:
            print(link, end=" , ")
            out.append(link)    
    return out
