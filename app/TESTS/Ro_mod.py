import networkx as nx
import pulp
import random
import numpy as np
import matplotlib.pyplot as plt

def image_networkx(nodes = 40, edges = 3, source = 0, target = 39):
    g = nx.to_directed(nx.barabasi_albert_graph(nodes, edges))
    nx.draw(g, with_labels=True)
    plt.savefig("test")
    print("oui")

    dict_capa = {}
    for i, j in g.edges:
        dict_capa[i, j] = dict_capa[j, i] = round(random.uniform(1.0, 20.0), 0)
    
    nx.set_edge_attributes(g, dict_capa, 'capacity')
    
    dict_used = {}
    for i, j in g.edges:
        dict_used[i, j] = dict_used[j, i] = min(round(random.uniform(0.0, 15.0), 0),dict_capa[i, j])
    
    nx.set_edge_attributes(g, dict_used, 'used')
    
    dict_ratio = {}
    for i, j in g.edges:
        dict_ratio[i, j] = dict_ratio[j, i] = dict_used[i, j]/dict_capa[i, j]
    
    nx.set_edge_attributes(g, dict_ratio, 'ratio')
    
    dict_delay = {}
    for i, j in g.edges:
        dict_delay[i, j] = dict_delay[j, i] = round(random.uniform(1.0, 20.0), 2)
    
    nx.set_edge_attributes(g, dict_delay, 'delay')
    
    i,j = zip(*g.edges)
    unique_i = np.unique(i)
    list_ratio = []
    for u_i in unique_i:
      temp_dict = {}
      for i, j in g.edges:
        if u_i==i:
          temp_dict["i"] = i
          temp_dict["j"] = j
          temp_dict["ratio"] = dict_ratio[i,j]
          list_ratio.append(*zip([list(temp_dict.values())[2]],[list(temp_dict.values())[0]],[list(temp_dict.values())[1]]))
    
    list_ratio_i = (sorted(list_ratio, key=lambda element: (element[1],element[0])))
    list_ratio_j = (sorted(list_ratio, key=lambda element: (element[2],element[0])))
    
    dict_score = {}
    score = 1
    prev_ratio = -1
    prev_i = 0
    for ratio,i,j in list_ratio_i:
      if ratio != prev_ratio:
        score += 1
      prev_ratio = ratio
      if (prev_i != i):
        score = 0
        prev_i = i
      dict_score[i, j] = score
    
    score = 1
    prev_ratio = -1
    prev_j = 0
    for ratio,i,j in list_ratio_j:
      if ratio != prev_ratio:
        score += 1
      prev_ratio = ratio
      if (prev_j != j):
        score = 0
        prev_j = j
      dict_score[j, i] = score
    
    nx.set_edge_attributes(g, dict_delay, 'score')
    
    # instantiate
    # instantiate
    list_keys = ['shortest_path','min_delay','min_banwidth_sum','min_banwidth_square_sum','min_score','min_square_score']
    dict_prob = {}
    dict_prob = dict_prob.fromkeys(list_keys)
    
    opti_path = {}
    opti_path = dict([(key, []) for key in list_keys])
    # binary variable to state a link is chosen or not
    for keys,prob in dict_prob.items():
      prob = pulp.LpProblem("%s" % keys, pulp.LpMinimize)
      var_dict = {}
      for (i, j) in g.edges:
          x = pulp.LpVariable("%s_(%s_%s)" % (keys,i,j), cat=pulp.LpBinary)
          var_dict[i, j] = x
      bdw = 1
    
    # objective function
      if keys == "shortest_path":
        prob += pulp.lpSum(var_dict[i, j] for i, j in g.edges), "Sum Node Count"
      elif keys == "min_delay":
        prob += pulp.lpSum([dict_delay[i, j] * var_dict[i, j] for i, j in g.edges]), "Sum delay"
      elif keys == "min_banwidth_sum":
        prob += pulp.lpSum([dict_ratio[i, j] * var_dict[i, j] for i, j in g.edges]), "Sum bandwidth ratio"
      elif keys == "min_banwidth_square_sum":
        prob += pulp.lpSum([dict_ratio[i, j] ** 20 * var_dict[i, j] for i, j in g.edges]), "Sum square bandwidth ratio"
      elif keys == "min_score":
        prob += pulp.lpSum([dict_score[i, j] * var_dict[i, j] for i, j in g.edges]), "Sum score"
      elif keys == "min_square_score":
        prob += pulp.lpSum([(dict_score[i, j] ** 20 * var_dict[i, j]) for i, j in g.edges]), "Sum square score"
        
    # constraints
      for node in g.nodes:
          rhs = 0
          if node == source:
              rhs = -1
          elif node == target:
              rhs = 1
          prob += pulp.lpSum([var_dict[i, k] for i, k in g.edges if k == node]) - pulp.lpSum([var_dict[k, j] for k, j in g.edges if k == node]) == rhs
    
    # constraints on capacity
      for i,k in g.edges:
        prob += var_dict[i, k]*bdw + dict_used[i,k]  <= dict_capa[i,k]
    
    # solve
      prob.solve()
      print("\n\n" + str(keys))
      print(pulp.LpStatus[prob.status])
      print(pulp.value(prob.objective))
      for link in g.edges:
          if var_dict[link].value() == 1.0:
              print(link, end=" , ")
              opti_path[keys].append(link)
    
    for key,path in opti_path.items():
      res = [[ i for i, j in path ], 
           [ j for i, j in path ]] 
      un_res = list()
      for i in res[0]:
        un_res.append(i)
      for i in res[1]:
        if i not in un_res:
          un_res.append(i) 
      print(un_res)
      sg = g.subgraph(un_res)
      nx.draw(sg, with_labels=True)
      
      plt.savefig(key)
      plt.show()
    
image_networkx(nodes = 40, edges = 3, source = 0, target = 1)
    
    
    
