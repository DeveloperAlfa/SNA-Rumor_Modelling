# -*- coding: utf-8 -*-
"""


@author: Developer Alfa
"""
import subprocess
import sys

def install(package):
    subprocess.call([sys.executable, "-m", "pip", "install", package])

install("python-louvain")
install("networkx")
import community
import networkx as nx
import matplotlib.pyplot as plt


G = nx.read_edgelist(path = "C:/Users/Samyak Aggarwal/Desktop/facebook_combined.txt", create_using = nx.Graph(), nodetype = int);

partition = community.best_partition(G)

#drawing
size = float(len(set(partition.values())))
pos = nx.spring_layout(G)
count = 0.
'''for com in set(partition.values()) :
    count = count + 1.
    list_nodes = [nodes for nodes in partition.keys()
                                if partition[nodes] == com]
    nx.draw_networkx_nodes(G, pos, list_nodes, node_size = 20,
                                node_color = str(count / size))


plt.show()'''

V_gate = [];
E_gate = [];
dict1 = {};
for edge in G.edges:
    if(partition[edge[0]] != partition[edge[1]]):
        a = min(partition[edge[0]], partition[edge[1]]);
        b = max(partition[edge[0]], partition[edge[1]]);
        s = str(a)+"-"+str(b);
        if(s not in dict1):
            V_gate.append(a);
            V_gate.append(b);
            E_gate.append(edge);
            dict1[s]  = edge;
gate = nx.Graph(E_gate)
pos2 = nx.spring_layout(gate)
nx.draw(gate, pos2, node_size = 20)
