import pynauty as nauty
import igraph as igraph
#from igraph import *

#g = nauty.Graph(number_of_vertices=15, directed=False, adjacency_dict = {
#    0: [1, 4, 5, 6],
#    1: [0, 2, 7, 8],
#    2: [1, 3, 9, 10],
#    3: [2, 4, 11, 12],
#    4: [0, 3, 13, 14],
#    5: [0, 6],
#    6: [0, 5],
#    7: [1, 8],
#    8: [1, 7],
#    9: [2, 10],
#    10: [2, 9],
#    11: [3, 12],
#    12: [3, 11],
#    13: [4, 14],
#    14: [4, 13],
#    },
#)

# autoMorphismGroup = nauty.autgrp(g)
# print(autoMorphismGroup)

matrix = [
    [1, 1, 0, 0, 0, 0],
    [1, 0, 1, 0, 0, 0],
    [1, 0, 0, 1, 0, 0],
    [0, 1, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 1],
    [0, 0, 1, 1, 0, 0],
    [0, 0, 0, 0, 1, 1],
]

# Taking a matrix a construct the bipartite graph of its
# Assuming that A is well-formed and non-empty
def construct_bi(A):
    numConstraints = len(A)
    numVars = len(A[0])
    g = nauty.Graph(numVars + numConstraints)
    ig = igraph.Graph()
    ig.add_vertices(numVars + numConstraints)
    ig.vs["type"] = 0
    ig.vs[numVars:]["type"] = 1
    for i in range(0, numVars):
        for j in range(0, numConstraints):
            if (A[j][i] == 1):
                g.connect_vertex(i, numVars + j)
                ig.add_edges([(i,numVars + j)])

    print(g)
    #igraph.plot(ig)
    return(g, ig)


biGraphs = construct_bi(matrix)

nautyGraph = biGraphs[0]
ig = biGraphs[1]

colour_dict = {0: "blue", 1: "red"}
ig.vs["color"] = [colour_dict[t] for t in ig.vs["type"]]
ig.vs["label"] = [i for i in range(0, 13)]
visual_style = {}
visual_style["vertex_size"] = 40
igraph.plot(ig, layout="bipartite",**visual_style)
print(biGraphs)

#print("Going to find and print the automorphism group")
autoMorphismGroup = nauty.autgrp(nautyGraph)
print(autoMorphismGroup)



exampleGraph = igraph.Graph()
exampleGraph.add_vertices(6)
exampleGraph.add_edges([(0, 1), (0,2), (0, 3), (1, 4), (1, 5), (2, 3), (4, 5)])
exampleGraph.vs["label"] = [i for i in range(0, 6)]
exampleGraph.vs["type"] = 0
exampleGraph.vs[2:]["type"] = 1
#exampleGraph.vs["color"] = [colour_dict[t] for t in exampleGraph.vs["type"]]
exampleGraph.es["label"] = [1]*7
exampleGraph.es[5:]["label"] = [2]*2

igraph.plot(exampleGraph, layout= "kk", **visual_style)


#subC = igraph.Graph()
#subC.add_vertices(2)
#subC.add_edges([(0, 1)])
#subC.vs["label"] = [i+1 for i in range(0, 2)]
#igraph.plot(subC, layout= "kk", **visual_style)

#subB = igraph.Graph()
#subB.add_vertices(3)
#subB.add_edges([(0, 1), (0,2), (1, 2)])
#subB.vs[0]["label"] = 1
#subB.vs[1]["label"] = 4
#subB.vs[2]["label"] = 5
#igraph.plot(subB, layout= "kk", **visual_style)


#from graph import *
#>>> g = Graph(6)
#>>> g.add_edges([(0,1), (0,2), (0,3), (1,4), (1,5), (2,3), (4,5)], [1, 1, 1, 1, 1, 2, 2])
#>>> g.plot()
