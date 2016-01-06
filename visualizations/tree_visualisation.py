"""
Query for data extraction:

SELECT DISTINCT
ot.tsn, tu.parent_tsn, tu.complete_name
FROM organism
Cross JOIN organism_tree(latin_name) AS ot
JOIN itis.taxonomic_units as tu ON tu.tsn = ot.tsn

Specific query for only some organisms:

SELECT DISTINCT
ot.tsn, tu.parent_tsn, COALESCE((SELECT name FROM organism_name WHERE id_language = 1 AND id_organism = organism.id_organism AND rank_id = 220), tu.complete_name)
FROM organism
Cross JOIN organism_tree(latin_name) AS ot
JOIN itis.taxonomic_units as tu ON tu.tsn = ot.tsn
WHERE id_organism IN (65, 78,85, 86, 13, 15, 402, 395, 106, 16);
"""
import csv
import sys

# To prevent some UTF-8 related issues
reload(sys)
sys.setdefaultencoding("utf-8")

#aaaaaaaaaaaaaaaaaaa


import pydot # import pydot or you're not going to get anywhere my friend :D

names = {}

graph = pydot.Dot(graph_type='graph')
with open('../data/processed/taxonomy-tree.csv', 'rb') as data:
    parsed = list(csv.reader(data, delimiter=','))
    for row in parsed:
        names[int(row[0])] = str(row[2]).capitalize()

    for row in parsed:
        if int(row[0]) in  names:
            name1 = names[int(row[0])]
        else:
            name1 = int(row[0])
        if int(row[1]) in  names:
            name2 = names[int(row[1])]
        else:
            name2 = int(row[1])

        if name2 == 0:
            continue
        edge = pydot.Edge(name1, name2)
        graph.add_edge(edge)

graph.write_png('tree.png')

##bbbbbbbbbbbbbbbbbbbbb