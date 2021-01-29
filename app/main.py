from fastapi import FastAPI 
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from starlette.responses import StreamingResponse

import networkx as nx
import pulp 
import numpy as np 

import matplotlib
import matplotlib.pyplot as plt

import codecs
import random
import io

matplotlib.use('Agg')

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

db = []
path = []
##############################################################
# Read index.html file which which is the home page
@app.get('/', response_class=HTMLResponse)
async def index():
    # find file in static
    file = codecs.open("static/index.html", "r")
    # make the page appear as the response class is HTMLResponse
    return file.read()

#############################################################
# go to this after the user has chosen to create its graph
@app.get('/generate/{nodes_edges}', response_class=HTMLResponse)
def image_nertworkx(nodes:int = 30, edges:int  = 3):
    g = nx.to_directed(nx.barabasi_albert_graph(nodes, edges))
    nx.draw(g, with_labels=True)
    plt.savefig("images/original.jpg")
    plt.close()
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

    nx.set_edge_attributes(g, dict_score, 'score')

    if len(db) > 0 :
        db.pop(0)
    db.append(nx.to_dict_of_dicts(g))
    
    file = codecs.open("static/graph_view.html", "r")
    return file.read()


@app.get('/graph')
async def get_graph():
    return db

@app.get("/vector_image")
def image_endpoint():
    file_like = open("images/original.jpg", mode="rb")
    return StreamingResponse(file_like, media_type="image/jpg")

@app.get("/opti_image")
def image_endpoint():
    file_like = open("images/opti_image.jpg", mode="rb")
    return StreamingResponse(file_like, media_type="image/jpg")

@app.get('/generate_path/{source_target}',response_class=HTMLResponse)
async def opti_path(source:int = 0, target:int  = 10):
    g = nx.Graph(db[0])
    list_keys = ['shortest_path','min_delay','min_banwidth_sum','min_banwidth_square_sum','min_score'] #,'min_square_score'
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
            prob += pulp.lpSum([g.edges[i,j]['delay'] * var_dict[i, j] for i, j in g.edges]), "Sum delay"
        elif keys == "min_banwidth_sum":
            prob += pulp.lpSum([g.edges[i,j]['ratio'] * var_dict[i, j] for i, j in g.edges]), "Sum bandwidth ratio"
        elif keys == "min_banwidth_square_sum":
            prob += pulp.lpSum([g.edges[i,j]['ratio'] ** 20 * var_dict[i, j] for i, j in g.edges]), "Sum square bandwidth ratio"
        elif keys == "min_score":
            prob += pulp.lpSum([g.edges[i,j]['score'] * var_dict[i, j] for i, j in g.edges]), "Sum score"
#        elif keys == "min_square_score":
#            prob += pulp.lpSum([(g.edges[i,j]['score'] ** 20 * var_dict[i, j]) for i, j in g.edges]), "Sum square score"
            
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
            prob += var_dict[i, k]*bdw + g.edges[i,k]['used']  <=g.edges[i,k]['capacity']

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
        res = [[i for i, j in path], 
        [j for i, j in path]] 
        un_res = list()
        for i in res[0]:
            un_res.append(i)
        for i in res[1]:
            if i not in un_res:
                un_res.append(i) 

    print(un_res)
    print("key : {}".format(key))
    sg = g.subgraph(un_res)
    nx.draw(sg, with_labels=True)
    plt.savefig("images/opti_image.jpg")
    plt.close()

    if pulp.LpStatus[prob.status] != 'Infeasible'  :
        file = codecs.open("static/path_view.html", "r")
        return file.read()
    else: return ('Infeasible')