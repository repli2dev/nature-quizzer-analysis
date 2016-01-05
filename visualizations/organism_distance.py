import networkx as nx
import matplotlib.pyplot as plt
import csv
import sys

# To prevent some UTF-8 related issues
reload(sys)
sys.setdefaultencoding("utf-8")

graph = nx.Graph()
# Directed graph instead?
with open('../data/organism_distance.csv', 'rb') as data:
    parsed = csv.reader(data, delimiter=';')
    for row in parsed:
        graph.add_node(row[0]) #, name=str(row[0])
        graph.add_node(row[1])
        graph.add_edge(row[0], row[1], weight=int(row[2]));


elarge=[(u,v) for (u,v,d) in graph.edges(data=True) if d['weight'] >10]
esmall=[(u,v) for (u,v,d) in graph.edges(data=True) if d['weight'] <=10]

pos=nx.spring_layout(graph) # positions for all nodes

# nodes
nx.draw_networkx_nodes(graph,pos,node_size=700)

# edges
nx.draw_networkx_edges(graph,pos,edgelist=elarge,
                       width=6, alpha=0.5)
nx.draw_networkx_edges(graph,pos,edgelist=esmall,
                       width=1,alpha=0.25,edge_color='b',style='dashed')

# labels
nx.draw_networkx_labels(graph,pos,font_size=20,font_family='sans-serif')

plt.axis('off')
plt.savefig("weighted_graph.png") # save as png
plt.show() # display