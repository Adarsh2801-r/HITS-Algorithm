import numpy as np
import networkx as nx #pip install networkx
import matplotlib.pyplot as plt
import scipy
from scipy import integrate

# Visualizing the given web graph
web_graph = nx.read_gpickle("web_graph.gpickle")
print(web_graph)
#get the 50th page content
node_index = 3
print(web_graph.nodes[node_index]['page_content'])
pos = {i: web_graph.nodes[i]['pos'] for i in range(len(web_graph.nodes))}
nx.draw(web_graph, pos)
plt.show()

# Getting adjacency matrix of the graph
A = nx.adjacency_matrix(web_graph).todense()


linked = {}
linking = {}

for i in range(0,100):
	linking[i] = []
	linked[i] = []

for i in range(0,100):
	for j in range(0,100):
		if A[i,j]==1:
			linking[i].append(j)
			linked[j].append(i)


print(linked[0])
print(linking[0])

# Generating root set from the query
query = input("Enter query:")
base_set = []
root_set = []
for node_idx in range(0,100):
	if query.lower() in web_graph.nodes[node_idx]['page_content'].lower().split():
		root_set.append(node_idx)


print("Root set : " + str(root_set))

# Generating base set from root set
for node in root_set:
	base_set.append(node)
	base_set.extend(linking[node])
	base_set.extend(linked[node])

print("Base Set : " + str(base_set))

# Making the subset graph
subset_size = len(base_set)
sub_adj = np.zeros([subset_size,subset_size])
y  = 0
for i in base_set:
	x = 0
	for j in base_set:
		if A[i,j]==1:
			sub_adj[x,y]=1
		x+=1
	y += 1

V1 = sub_adj@sub_adj.T
V2 = sub_adj.T@sub_adj

 
print(V1)

# Calculating hub scores and authority scores
h = scipy.linalg.eig(V1,left=True,right=False)[1][:,0]
a = scipy.linalg.eig(V2,left=True,right=False)[1][:,0]
h = (h/np.sum(h))
a = (a/np.sum(a))

print("Hub scores : " + str(h))
print("Authority scores : "+str(a))

