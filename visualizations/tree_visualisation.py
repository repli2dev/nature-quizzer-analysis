"""
Query for data extraction:

SELECT DISTINCT
ot.tsn, tu.parent_tsn, tu.complete_name
FROM organism
Cross JOIN organism_tree(latin_name) AS ot
JOIN itis.taxonomic_units as tu ON tu.tsn = ot.tsn
"""
import csv
import networkx
import sys
import matplotlib.pyplot as plt

# To prevent some UTF-8 related issues
reload(sys)
sys.setdefaultencoding("utf-8")

graph = networkx.DiGraph()
# Directed graph instead?
with open('../data/tree.csv', 'rb') as data:
    parsed = csv.reader(data, delimiter=',')
    for row in parsed:
        graph.add_node(row[0], label='X')
        graph.node[row[0]]['sep'] = 10
        graph.add_node(row[1])
        #graph.node[row[1]]['label'] = str(row[3])
        if (int(row[1]) != 0): graph.add_edge(row[1], row[0])

g=graph
g
pos = networkx.graphviz_layout(g, prog='dot')
for i in pos:
    pos[i] = pos[i][0] * 2, pos[i][1] * 2
#pos = networkx.spring_layout(g)
networkx.draw(g,pos, node_size=2, with_labels=True, node_color='b', linewidths=0)
plt.show()
"""
networkx.write_dot(graph,'test.dot')
plt.title("draw_networkx")
pos=networkx.graphviz_layout(graph,prog='dot')
networkx.draw(graph,pos,with_labels=True,arrows=True)
plt.show()
"""