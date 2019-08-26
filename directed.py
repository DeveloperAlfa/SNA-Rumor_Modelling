# -*- coding: utf-8 -*-# -*- coding: utf-8 -*-
"""
Created on Sun Jan 13 10:50:34 2019

@author: Developer Alfa
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 10:10:28 2018

@author: Developer Alfa
"""
import subprocess
import sys
import math
def install(package):
    subprocess.call([sys.executable, "-m", "pip", "install", package])

install("python-louvain")
install("networkx")

import csv
import networkx as nx
import matplotlib.pyplot as plt
import queue
import random




csvFile = open('C:/Users/Samyak Aggarwal/Desktop/Data/stats_ds_sanjay_sir.csv', 'a')
csvWriter = csv.writer(csvFile)
G = nx.read_edgelist(path = "C:/Users/Samyak Aggarwal/Desktop/Data/amz.txt")
'''partition = community.best_partition(G)'''   

G.remove_edges_from(nx.selfloop_edges(G))
#drawing
'''size = float(len(set(partition.values())))
pos = nx.spring_layout(G)
count = 0.
for com in set(partition.values()) : 
    count = count + 1.
    list_nodes = [nodes for nodes in partition.keys()
                                if partition[nodes] == com]
    nx.draw_networkx_nodes(G, pos, list_nodes, node_size = 20,
                                node_color = str(count / size))


plt.show()'''
nodes = list(G.nodes())
edges = list(G.edges())
adj = []
node_degree = 0
capability = {}
k = int(input("Input the number of infectors: "))
S = int(input("Input the number of times SIR should average out: "))
T = int(input("Input the timestamps: "))
beta = float(input("Input beta: "))
selected = []
forbidden = []
for i in range(len(nodes)):
    capability[nodes[i]] = [0, 1]
    neigh = list(G.neighbors(nodes[i]))
    adj.append(neigh)
    node_degree+=len(neigh)

node_degree/=len(nodes)
val = 1/node_degree

def ex():
    ks = nx.core_number(G)
    icc ={}
    Nodes = list(G.nodes())
    for node in Nodes:
        icc[node] = 0
        n = G.neighbors(node)
        for neighbor in n:
            icc[node]+=ks[neighbor]
    #print(icc)
            
    ex = {}
    for node in Nodes:
        ex[node]  = 0
        n = G.neighbors(node)
        for neighbor in n:
            ex[node]+=icc[neighbor]
    return ex

#Vote Rank
#extended = ex()
    
def max_normalize(dic, nodes):
    minn = 1000000000;
    maxx = -1
    for node in nodes:
        minn = min(minn, dic[node])
        maxx = max(maxx, dic[node])
    for node in nodes:
        dic[node] = (dic[node])/(maxx-minn)
        
ext = ex()
kshell = nx.core_number(G)
#max_normalize(ext, list(G.nodes()))
for j in range(k):
    best_node = -1
    max_votes = -1
    for i in range(len(nodes)):
        capability[nodes[i]][0] = 0
    for i in range(len(nodes)):
        for node in adj[i]:
            capability[nodes[i]][0]+=capability[node][1]
    dic = {}
    for node in nodes:
        dic[node] = capability[node][0]
    max_normalize(dic, list(G.nodes()))
    for node in nodes:
        if(dic[node]*kshell[node]>max_votes and node not in selected):
            max_votes = dic[node]*kshell[node]
            best_node = node
    capability[best_node][1] = 0
    selected.append(best_node)
    forbidden.append(best_node)
    for node in list(G.neighbors(best_node)):
        capability[node][1]-=val
        forbidden.append(node)
    s = ("Round "+ str(j+1) + " and best node is " + str(best_node) + " with " + str(max_votes))
    #print(s)


def voteRank(G, n):
    capability = {}
    Nodes = list(G.nodes())
    totdeg = 0
    for node in Nodes:
        capability[node] = [0, 1]
        totdeg+=G.degree(node)
    totdeg/=len(Nodes)
    val = 1/totdeg
    selected = []
    for i in range(n):
        for node in Nodes:
            capability[node][0] = 0
        bes = 0
        bestnode = -1
        for node in Nodes:
            allnodes = list(G.neighbors(node))
            for neig in allnodes:
                capability[node][0]+=capability[neig][1]
            if(capability[node][0]>bes and node not in selected):
                bes = capability[node][0]
                bestnode = node
        selected.append(bestnode)
        capability[bestnode][1] = 0
        neighbors = list(G.neighbors(bestnode))
        for node in neighbors:
            capability[node][1]-=val
    return selected
def WvoteRank(G, n):
    capability = {}
    Nodes = list(G.nodes())
    totdeg = 0
    for node in Nodes:
        capability[node] = [0, 1]
        totdeg+=G.degree(node)
    totdeg/=len(Nodes)
    val = 1/totdeg
    selected = []
    for i in range(n):
        for node in Nodes:
            capability[node][0] = 0
        bes = 0
        bestnode = -1
        for node in Nodes:
            allnodes = list(G.neighbors(node))
            for neig in allnodes:
                capability[node][0]+=capability[neig][1]
            capability[node][0]=math.sqrt(int(capability[node][0]*G.degree(node)))
            if(capability[node][0]>bes and node not in selected):
                bes = capability[node][0]
                bestnode = node
        selected.append(bestnode)
        capability[bestnode][1] = 0
        neighbors = list(G.neighbors(bestnode))
        for node in neighbors:
            capability[node][1]-=val
    return selected
def voteRankf(G, n):
    ksof = nx.core_number(G);
    max_normalize(ksof, list(G.nodes()))
    icc = {}
    Nodes = list(G.nodes())
    for node in Nodes:
        icc[node] = 0
        adj = G.neighbors(node)
        for a in adj:
            icc[node]+=ksof[a]
    max_normalize(icc, list(G.nodes()))
    #print(icc)
    capability = {}
    Nodes = list(G.nodes())
    totdeg = 0
    for node in Nodes:
        capability[node] = [0, 1]
        totdeg+=G.degree(node)
    totdeg/=len(Nodes)
    val = 1/totdeg
    selected = []
    forbidden = []
    for i in range(n):
        for node in Nodes:
            capability[node][0] = 0
        bes = 0
        bestnode = -1
        for node in Nodes:
            allnodes = list(G.neighbors(node))
            for neig in allnodes:
                capability[node][0]+=(capability[neig][1]*icc[neig])
            if(capability[node][0]>bes and node not in selected):
                bes = capability[node][0]
                bestnode = node
        selected.append(bestnode)
        forbidden.append(bestnode)
        capability[bestnode][1] = 0
        neighbors = list(G.neighbors(bestnode))
        for node in neighbors:
            capability[node][1]-=(val) 
            forbidden.append(bestnode)
    return selected

def SIR_Neeraj(g, spreaders, beta):
    infected= spreaders 
    status={}
    #print("SIR")
    for i in g.nodes():
        status.update({i:0})
    #del status['key']
    
        
    for i in infected:
        status[i]=1;
          
    n=g.number_of_nodes() 
    infected_scale=[0 for i in range(T)]
    infected_nodes=len(infected)
    recovered_nodes=0
    infected_scale.append((infected_nodes+recovered_nodes)/n)
    infected=spreaders
    time=0
    while(len(infected)>0 and time < T):
        susceptible_to_infected=[]
        time=time+1
        #print("time=",time)
        #print("infected=",infected)
        for infected in infected:
            susceptible=[]
            status[infected]=2
            for neighbor in g.neighbors(infected):
                if(status[neighbor]==0):
                    susceptible.append(neighbor)
            #print("susceptible=",susceptible)        
            total_susceptible=len(susceptible)
            #print("total no of susceptible nodes are=",total_susceptible)
            no_of_susceptible_to_infected=round(beta*total_susceptible)
            #print('after calculating probability=', no_of_susceptible_to_infected)
            while no_of_susceptible_to_infected>0:
                random_index=random.randint(0,total_susceptible-1)
                if susceptible[random_index] not in susceptible_to_infected:
                 susceptible_to_infected.append(susceptible[random_index])
                 status[susceptible[random_index]]=1
                 no_of_susceptible_to_infected=no_of_susceptible_to_infected-1
                 #print("infected to be =",susceptible[random_index])
        infected_nodes=len(susceptible_to_infected)
        recovered_nodes=len(infected)
        infected_scale[time] = ((infected_nodes+recovered_nodes))
        infected=susceptible_to_infected      
    return infected_scale

def ftToftc(ft):
    ftc = [0 for i in range(0, T+1)]
    for i in range(T):
        ftc[i+1] = ft[i] + ftc[i]
    return ftc

def SIR(G, selected, beta):
    print("SIR")
    ft = [0 for i in range(T)]
    Q = queue.Queue(maxsize=len(list(G.nodes())))
    recovered = []
    infected = []
    for node in selected:
        Q.put(node)
        infected.append(node)
    t = 0
    
    
    while(t<T):
        
        tot = []
        while(Q.empty()==False):
            curr = Q.get()
            if curr in recovered:
                continue
            recovered.append(curr)
            ne = list(G.neighbors(curr))
            random.shuffle(ne)
            neighbors = int(len(ne) * beta) + 1
            count = 0
            idx = 0
            while(count<neighbors and idx < len(ne)):
                if(ne[idx] not in recovered and ne[idx] not in tot):
                    tot.append(ne[idx])
                    count+=1
                idx+=1
        for i in tot:
            Q.put(i)
        tot.clear()
        ft[t] = len(recovered)
        t+=1
    return ft



def Multi_SIR(n, G, selected, beta):
    ft = [0 for i in range(T)]
    for i in range(n):
        fti = SIR_Neeraj(G, selected, beta)
        for j in range(T):
            ft[j]+=fti[j]
    for i in range(T):
        ft[i] = ft[i]/n;
        ft[i] = ft[i]/len(list(G.nodes()))
    return ft


def select_n(nodes, dic, n):
    selected = []
    forbidden = []
    for i in range(n):
        best = 0
        bestnode = -1
        for node in nodes:
            if node not in forbidden and dic[node]>best:
                best = dic[node]
                bestnode = node
        selected.append(bestnode)
        forbidden.append(bestnode)
        for i in list(G.neighbors(bestnode)):
            forbidden.append(i)
    return selected



#page = nx.pagerank(G)
page_selected = select_n(nodes, nx.pagerank(G), k)
#degree_selected = select_n(nodes, nx.degree_centrality(G), k)
#eigen_selected = select_n(nodes, nx.eigenvector_centrality(G), k)
#extended_selected = select_n(nodes, ext, k)
vote_selected = voteRank(G, k)
votef_selected = voteRankf(G, k)
Wvote_selected = WvoteRank(G, k)
#ks_selected = select_n(nodes, nx.core_number(G), k)

print("Running SIR")
hybrid = Multi_SIR(S, G, selected, beta)
print(".")
pagerank = Multi_SIR(S, G, page_selected, beta)
#degree = Multi_SIR(S, G, degree_selected, beta)
#eigen = Multi_SIR(S, G, eigen_selected, beta)
vote = Multi_SIR(S, G, vote_selected, beta)
print(".")
votef = Multi_SIR(S, G, votef_selected, beta)
wvote = Multi_SIR(S, G, Wvote_selected, beta)
print(".")
#ks = Multi_SIR(S, G, ks_selected, beta)
#extended = Multi_SIR(S, G, extended_selected, beta)






print("plotting")
ftc_hybrid = ftToftc(hybrid)
ftc_pagerank = ftToftc(pagerank)
#ftc_degree = ftToftc(degree)
ftc_vote = ftToftc(vote)
#ftc_ks = ftToftc(ks)
ftc_votef = ftToftc(votef)
ftc_wvote = ftToftc(wvote)
#ftc_eigen = ftToftc(eigen)
#ftc_extended = ftToftc(extended)

plt.plot(range(T+1), ftc_hybrid, '--m*', label = "VoteRank*Kshell")
plt.plot(range(T+1), ftc_pagerank, '-.gd', label = "PageRank", markerfacecolor = 'w')
#plt.plot(range(T+1), ftc_degree, '-.rs', label = "Degree")
#plt.plot(range(T+1), ftc_eigen, '-bs', label = "Eigen", markerfacecolor = 'w')
plt.plot(range(T+1), ftc_vote, '-.co', label = "VoteRank", markerfacecolor = 'w')
#plt.plot(range(T+1), ftc_ks, '-y*', label = "K Shells", markerfacecolor = 'w')


plt.plot(range(T+1), ftc_votef, '-kp', label = "Improved VoteRank", markerfacecolor = 'w')
plt.plot(range(T+1), ftc_wvote, '-rD', label = "WVoteRank", markerfacecolor = 'w')
plt.xlabel('Time')
plt.ylabel('F(tc)')
plt.legend(loc='best')
n = len(list(G.nodes()))
for i in range(T+1):
    print((ftc_votef[i] - ftc_vote[i])*n)
plt.show()

